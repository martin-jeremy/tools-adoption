import os
from prefect import flow
from prefect.logging import get_run_logger


PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "transform/")
PROFILES_DIR = os.getenv("DBT_PROFILES_DIR", "transform/")
DBT_DUCKDB_PATH = os.getenv("DBT_DUCKDB_PATH", "data/analytics.db")

@flow(name="dbt Transformation Flow")
def dbt_flow():
    logger = get_run_logger()
    logger.info("Starting dbt transformation flow")

    import subprocess
    env = os.environ.copy()
    subprocess.run(["dbt", "run", "--profiles-dir", PROFILES_DIR, "--project-dir", PROJECT_DIR],check=True, env=env)

@flow(name="dbt Cleaning Flow")
def dbt_clean():
    logger = get_run_logger()
    logger.info("Starting dbt cleaning flow")

    import subprocess
    env = os.environ.copy()
    subprocess.run(
        ["dbt", "clean", "--profiles-dir", PROFILES_DIR, "--project-dir", PROJECT_DIR],
        check=True,
        env=env,
    )

if __name__ == "__main__":
    dbt_flow()
    # dbt_clean()