import duckdb
import yaml
import pandas as pd
from prefect import flow, task
from prefect.logging import get_run_logger
import requests
from pathlib import Path

DB_PATH = "data/analytics.db"
CONFIG_PATH = "tools.yml"

def load_config(path: str = CONFIG_PATH) -> dict:
    """Charge la liste des outils à monitorer"""
    return yaml.safe_load(Path(path).read_text())

@task(name="github-stars", retries=3)
def fetch_github_stars(repo: str):
    """Récupère le nombre de star d'un repos Github"""
    logger = get_run_logger()
    logger.info(f"Fetching stars for {repo}")
    try:
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error fetching stars for {repo}: {e}")
        return None
    return {
        "provider": "Github",
        "tool_name": data["name"],
        "tool_desc": data["description"],
        "tool_url": data["html_url"],
        "metric_name": "stars",
        "value": data["stargazers_count"],
        "collected_at": pd.Timestamp.now()
    }

@task(name="pypi-dl", retries=3)
def fetch_pypi_dl(package: str):
    """Récupère le nombre de téléchargements d'un package PyPI"""
    logger = get_run_logger()
    logger.info(f"Fetching downloads for {package}")
    try:
        url = f"https://pypistats.com/api/packages/{package}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error fetching stars for {package}: {e}")
        return None
    return {
        "provider": "PyPI Stats",
        "tool_name": data["metadata"]["name"],
        "tool_desc": data["metadata"]["summary"],
        "tool_url": data["metadata"]["home_page"],
        "metric_name": "downloads",
        "value": data["trend"][-1]['total_downloads'],
        "collected_at": pd.Timestamp.now()
    }

@task(name="save-to-duckdb")
def save_to_duckdb(data: dict | None):
    if data is None:
        get_run_logger().warning("Skipping None record")
        return

    Path(DB_PATH).parent.mkdir(exist_ok=True)

    data['last_check_at'] = data['collected_at']

    with duckdb.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS raw (
            provider      VARCHAR,
            tool_name     VARCHAR,
            tool_desc     VARCHAR,
            tool_url      VARCHAR,
            metric_name   VARCHAR,
            value         INTEGER,
            collected_at  TIMESTAMP,
            last_check_at TIMESTAMP
        )
        """)

        # Récupère la dernière valeur connue pour cet outil/métrique
        last = con.execute("""
            SELECT value FROM raw
            WHERE provider = ?
              AND tool_name = ?
              AND metric_name = ?
            ORDER BY collected_at DESC
            LIMIT 1
        """, [data['provider'], data['tool_name'], data['metric_name']]).fetchone()

        if last is None or last[0] != data["value"]:
            # Valeur nouvelle ou première insertion : INSERT complet
            data["last_check_at"] = data["collected_at"]
            con.execute("""
            INSERT INTO raw VALUES (
                $provider, $tool_name, $tool_desc, $tool_url,
                $metric_name, $value, $collected_at, $last_check_at
            )
            """, data)
        else:
            # Valeur inchangée : UPDATE last_check_at sur la dernière ligne
            con.execute(
                """
            UPDATE raw SET last_check_at = ?
            WHERE provider = ?
              AND tool_name = ?
              AND metric_name = ?
              AND collected_at = (
                  SELECT MAX(collected_at) FROM raw
                  WHERE provider = ?
                    AND tool_name = ?
                    AND metric_name = ?
              )
            """,
                [
                    [data["collected_at"]],
                    [data["provider"], data["tool_name"], data["metric_name"]],
                    [data["provider"], data["tool_name"], data["metric_name"]],
                ],
            )

@flow(name="ingest-flow")
def ingestion_flow(repos: dict):
    """Fonction principale du flux"""
    logger = get_run_logger()
    logger.info("Starting data ingestion flow")
    gh = [ rep for rep in [gh['repo'] for gh in repos.get('github')] ]
    pypi = [ pkg for pkg in [pypi['package'] for pypi in repos.get('pypi')] ]

    # Ingest
    try:
        # Concurrency problem: Quack could be a solution
        # save_to_duckdb.map(fetch_github_stars.map(gh))
        # save_to_duckdb.map(fetch_pypi_dl.map(pypi))
        for repo in gh:
            logger.info(f"Fetching stars for {repo}")
            stats = fetch_github_stars(repo)
            save_to_duckdb(stats)
        for pkg in pypi:
            logger.info(f"Fetching downloads for {pkg}")
            stats = fetch_pypi_dl(pkg)
            save_to_duckdb(stats)
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
    logger.info("Data ingestion flow completed")

if __name__ == "__main__":
    ingestion_flow(load_config())