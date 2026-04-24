# E-commerce Analytics Pipeline

An end-to-end batch ETL pipeline processing 541,909 transactional records from the 
UCI Online Retail Dataset using PySpark, DuckDB, dbt, and Docker.

## Architecture
Raw CSV → PySpark Cleaning → Parquet → DuckDB Warehouse → dbt Models → SQL Analytics → Tableau

## Tech Stack
- **Processing:** PySpark
- **Warehouse:** DuckDB
- **Transformation:** dbt (7 data quality tests)
- **Containerization:** Docker
- **Visualization:** Tableau Public
- **Orchestration:** Apache Airflow

## Pipeline Steps
1. **Ingest** — Download UCI Online Retail Dataset
2. **Clean** — PySpark silver-level cleaning (null filtering, invalid record removal, revenue computation)
3. **Export** — Output partitioned Parquet files
4. **Load** — Write to DuckDB analytics warehouse
5. **Transform** — dbt staging and mart models (daily revenue, top products, country revenue)
6. **Analyze** — SQL queries surfacing key business metrics
7. **Visualize** — Tableau dashboard

## Data Quality
7 automated dbt tests enforcing null and uniqueness constraints across all tables

## Dashboard
[View Tableau Dashboard](https://public.tableau.com/app/profile/xuan.zhang8153/viz/ecommerce_tableau_analysis/E-commerceRevenueDashboard)

## How to Run
1. Clone the repo
2. Build Docker container: `docker-compose up`
3. Run pipeline: `python run_pipeline.py`
4. Run dbt: `cd dbt_project && dbt run`
