import os
import duckdb
from pathlib import Path

if __name__ == "__main__":
    db_path = os.getenv("DBT_DUCKDB_PATH", 'data/analytics.db')
    datadir = Path(db_path).parent
    Path(datadir).mkdir(exist_ok=True)
    con = duckdb.connect(db_path, read_only=True)
    for table in ['fct_tools_adoption_daily', 'fct_tools_adoption_history', 'fct_tools_adoption_overall']:
        df = con.execute(f"SELECT * FROM {table}").df()
        df.to_parquet(f"data/{table}.parquet", index=False)
        print(f"{table}: {len(df)} rows exported")

    con.close()
