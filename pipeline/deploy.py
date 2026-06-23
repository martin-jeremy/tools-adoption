import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from pipeline.flows._01_extract_and_load import ingestion_flow, default_repos

if __name__ == "__main__":
    # .serve() permet d'exposer le flux en tant que service
    # sans avoir besoin de reconstruire une image docker
    ingestion_flow.serve(
        name='ingestion-flow',
        cron='0 0 * * *',
        parameters={'repos': default_repos}
    )