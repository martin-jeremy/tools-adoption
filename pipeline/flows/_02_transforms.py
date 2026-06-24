import os
from prefect import flow
from prefect.logging import get_run_logger

@flow(name="dbt Transformation Flow")
def dbt_flow():
    logger = get_run_logger()
    logger.info("Starting dbt transformation flow")

    import subprocess
    env = os.environ.copy()
    env["DBT_DUCKDB_PATH"] = "/data/analytics.db"
    project_dir = profiles_dir = "/opt/prefect/project/transform"
    subprocess.run(["dbt", "run", "--profiles-dir", profiles_dir, "--project-dir", project_dir],check=True, env=env)

@flow(name="dbt Cleaning Flow")
def dbt_clean():
    logger = get_run_logger()
    logger.info("Starting dbt cleaning flow")

    import subprocess
    env = os.environ.copy()
    env["DBT_DUCKDB_PATH"] = "/data/analytics.db"
    project_dir = profiles_dir = "/opt/prefect/project/transform"
    subprocess.run(
        ["dbt", "clean", "--profiles-dir", profiles_dir, "--project-dir", project_dir],
        check=True,
        env=env,
    )

if __name__ == "__main__":
    dbt_flow()
    dbt_clean()