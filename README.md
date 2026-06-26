# tools-adoption : Adopt a Tool !

> A data pipeline that tracks Modern Data Stack tool adoption, built with that very same Modern Data Stack. Yes, it's recursive. No, it's not an accident.

**[See it live →](https://martin-jeremy.github.io/tools-adoption)**

---

## What it does

Every 6 hours, GitHub Actions collects **GitHub stars** and **PyPI downloads** for the tools configured in `tools.yml`, stores them in DuckDB, transforms them with dbt, and updates an Evidence dashboard deployed on GitHub Pages.

No server. No cost. Artifacts (DB + Parquet) live on a `latest` GitHub Release.

```
GitHub API ─┐
            ├─► Prefect flow ─► DuckDB ─► dbt ─► Parquet ─► GitHub Release
PyPI API  ──┘                                                      │
                                                                   ▼
                                                         Evidence (GitHub Pages)
```

---

## Adding or removing a tool

Everything lives in `tools.yml` at the repo root:

```yaml
# tools.yml
github:
  - repo: duckdb/duckdb
  - repo: dbt-labs/dbt-core
  - repo: PrefectHQ/prefect
  - repo: slothflowlabs/duckle

pypi:
  - package: duckdb
  - package: dbt-core
  - package: prefect
```

Edit the file, commit, push. The pipeline runs within 6 hours. That's it.

---

## Using the dashboard without installing anything

**[martin-jeremy.github.io/tools-adoption](https://martin-jeremy.github.io/tools-adoption)**

The dashboard reads Parquet files directly from the GitHub Release on every page load. Data stays fresh without any intervention on your end.

---

## Running the pipeline locally

Prerequisites: Docker and Docker Compose.

```bash
git clone https://github.com/martin-jeremy/tools-adoption.git
cd tools-adoption
docker compose up -d
```

That's it. Nothind else to do.

- **Prefect UI** → [localhost:4200](http://localhost:4200)
- **Superset** → [localhost:8088](http://localhost:8088) (admin / admin)

The pipeline runs every 6 hours automatically. To trigger it manually from the Prefect UI: `main-orchestrator` → Run.

---

## For the curious

### Architecture

| Layer | Tool | Role |
|---|---|---|
| Orchestration | Prefect 3 | Scheduling, retries, observability |
| Ingestion | Python + requests | GitHub API, PyPI Stats API |
| Storage | DuckDB 1.5 | File-based analytical database |
| Transformation | dbt-duckdb 1.10 | Staging → Intermediate → Marts |
| Visualization (self-hosted) | Apache Superset | Local BI via Docker |
| Visualization (static) | Evidence | Generated dashboard, deployed to GitHub Pages |
| CI/CD | GitHub Actions | 6h pipeline + dashboard deployment |
| Persistence | GitHub Release `latest` | `analytics.db` + Parquet reloaded on every run |

### dbt models

```
sources.analytics.raw
  └── stg_analytics__raw                (view)
        └── int_analytics__lag_values   (view)  ← delta and % evolution via LAG()
        |     ├── fct_tools_adoption_daily       (table) ← snapshot: latest value per tool
        |     └── fct_tools_adoption_history     (table) ← full history for time series
        └── fct_tools_adoption_overall           (table) ← overview of all tools
```

### Why DuckDB as the primary storage?

The project tracks DuckDB adoption. Using anything else would have been ironic.

More seriously: DuckDB in file mode is more than sufficient for this volume (a few thousand rows), exports trivially to Parquet, and integrates natively with both dbt and Evidence (or Superset). The `.db` file is versioned on a GitHub Release and reloaded at every CI run — no remote database to maintain.

### Known limitation: DuckDB concurrency

In local file mode, DuckDB does not support concurrent writes. Ingestion is therefore sequential. The code says it plainly:

```python
# Concurrency problem: Quack could be a solution
```

[Quack](https://duckdb.org/quack/) (DuckDB's client-server protocol, HTTP transport) is a candidate fix down the road, but it's not yet available in DuckDB 1.5 and it needs to set up a server-side proxy.

---

## TODO

- [ ] **Streamlit frontend** — connected to the same Release Parquet files, for an interactive view (filters, per-tool drill-down). The goal is a source-agnostic frontend layer: same data, renderer chosen by use case.
- [ ] **Pydantic** — Data contract before ingestion.
- [ ] **dbt tests** — `schema.yml` with non-null and consistency checks on marts.
- [ ] **npm downloads** — track npm download counts for tools that also ship JS packages (dbt-osmosis, Evidence itself...).
- [ ] **Alerting** — flag abnormal metric drops (e.g. -20% downloads in a single day).

---

## Stack

Python 3.12 · DuckDB 1.5 · dbt-duckdb 1.10 · Prefect 3 · Evidence · Apache Superset · GitHub Actions · uv