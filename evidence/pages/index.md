---
title: Tools Adoption
full_width: true
---

```sql snapshot
select * from tools_adoption.daily
```

```sql github_stars
select * from tools_adoption.daily
where Metrics = 'stars'
order by Value desc
```

```sql pypi_downloads
select * from tools_adoption.daily
where Metrics = 'downloads'
order by Value desc
```

# tools-adoption : Adopt a Tool !

> A data pipeline that tracks Modern Data Stack tool adoption, built with that very same Modern Data Stack. Yes, it's recursive. No, it's not an accident.

Every 12 hours, GitHub Actions collects **GitHub stars** and **PyPI downloads** for a set of tools, stores them in DuckDB, transforms them with dbt, and updates this dashboard. No server. No cost. Artifacts (`analytics.db` + Parquet files) live on a GitHub Release `latest` and are reloaded on every run.

---

## Current Snapshot

### GitHub Stars

<BarChart
  data={github_stars}
  x=Name
  y=Value
  yAxisTitle="Stars"
  swapXY=true
/>

<DataTable data={github_stars} rows=10>
  <Column id=Name />
  <Column id=Value title="Stars" fmt=num0 />
  <Column id=Evolution title="Δ last run" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
</DataTable>

### PyPI Downloads

<BarChart
  data={pypi_downloads}
  x=Name
  y=Value
  yAxisTitle="Downloads"
  swapXY=true
/>

<DataTable data={pypi_downloads} rows=10>
  <Column id=Name />
  <Column id=Value title="Downloads" fmt=num0 />
  <Column id=Evolution title="Δ last run" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
</DataTable>

---

## How it works

```shell
GitHub API ─┐
            ├─► Prefect flow ─► DuckDB ─► dbt ─► Parquet ─► GitHub Release
PyPI API  ──┘                                                      │
                                                                   ▼
                                                      Evidence (GitHub Pages)
```

### Architecture

| Layer | Tool | Role |
|---|---|---|
| Orchestration | Prefect 3 | Scheduling, retries, observability |
| Ingestion | Python + requests | GitHub API, PyPI Stats API |
| Storage | DuckDB 1.5 | File-based analytical database |
| Transformation | dbt-duckdb 1.10 | Staging → Intermediate → Marts |
| Visualization | Evidence | Generated dashboard, deployed to GitHub Pages |
| CI/CD | GitHub Actions | 12h pipeline + dashboard deployment |
| Persistence | GitHub Release `latest` | `analytics.db` + Parquet reloaded on every run |

### dbt models

```shell
sources.analytics.raw
  └── stg_analytics__raw                (view)
        └── int_analytics__lag_values   (view)  ← delta and % evolution via LAG()
        │     ├── fct_tools_adoption_daily       (table) ← snapshot: latest value per tool
        │     └── fct_tools_adoption_history     (table) ← full history for time series
        └── fct_tools_adoption_overall           (table) ← overview of all tools
```

### Why DuckDB as the primary storage?

The project tracks DuckDB adoption. Using anything else would have been ironic.

More seriously: DuckDB in file mode is sufficient for this volume, exports trivially to Parquet, and integrates natively with both dbt and Evidence. The `.db` file is versioned on a GitHub Release and reloaded at every CI run — no remote database to maintain.

### Known limitation: DuckDB concurrency

In local file mode, DuckDB does not support concurrent writes. Ingestion is therefore sequential. The code says it plainly:

```python
# Concurrency problem: Quack could be a solution
```

[Quack](https://duckdb.org/docs/stable/extensions/quack.html) (DuckDB's client-server extension, HTTP transport) is a candidate fix down the road.

---

**Stack:** Python 3.12 · DuckDB 1.5 · dbt-duckdb 1.10 · Prefect 3 · Evidence · GitHub Actions · uv

**Source:** [github.com/martin-jeremy/tools-adoption](https://github.com/martin-jeremy/tools-adoption)