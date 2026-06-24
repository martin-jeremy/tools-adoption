FROM apache/superset:latest

USER root

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

RUN uv pip install duckdb-engine duckdb

USER superset