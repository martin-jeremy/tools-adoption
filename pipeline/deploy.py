import os
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from prefect import flow
from pipeline.flows._01_extract_and_load import ingestion_flow, load_config
from pipeline.flows._02_transforms import dbt_flow, dbt_clean

@flow(name="main-orchestrator")
def main_orchestrator():
    ingestion_flow(load_config())
    dbt_flow()
    dbt_clean()

if __name__ == "__main__":
    # .serve() permet d'exposer le flux en tant que service
    # sans avoir besoin de reconstruire une image docker
    main_orchestrator.serve(
        name='main-orchestrator',
        interval=21600 # chaque 6 heures
    )