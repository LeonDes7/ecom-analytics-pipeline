# E-commerce Analytics Pipeline

An end-to-end batch ETL pipeline processing 397,884 transactional records from the UCI Online Retail Dataset using PySpark, DuckDB, dbt, and Docker.

## Architecture
Raw Excel → Pandas Clean → PySpark (Docker) → Parquet → DuckDB Warehouse → dbt Models → SQL Analytics

## Tech Stack
- **Processing:** PySpark 4.0 (containerized via Docker)
- **Warehouse:** DuckDB
- **Transformation:** dbt (9 automated data quality tests)
- **Containerization:** Docker & Docker Compose
- **Visualization:** Tableau Public

## Pipeline Steps
1. **Extract** — Download UCI Online Retail Dataset (.xlsx)
2. **Inspect** — Profile raw data quality, schema, and completeness
3. **Clean** — Pandas silver-level cleaning (null filtering, cancellation removal, revenue derivation)
4. **PySpark Transform** — Distributed cleaning and partitioned Parquet export inside Docker
5. **Feature Engineering** — Build daily revenue, top products, and country revenue aggregates
6. **Parquet Export** — Persist cleaned transactions as columnar Parquet for warehouse layer
7. **DuckDB Load** — Bulk load analytics tables into DuckDB OLAP warehouse
8. **SQL Analytics** — Run 6 analytical queries surfacing $8.9M in revenue insights across 37 countries
9. **dbt Run** — Build 4 staging and mart models on top of Spark-generated Parquet
10. **dbt Test** — Execute 9 automated data quality assertions (null and uniqueness constraints)

## Data Quality
9 automated dbt tests enforcing not-null constraints across all staging and mart tables

## Dashboard
[View Tableau Dashboard](https://public.tableau.com/app/profile/xuan.zhang8153/viz/ecommerce_tableau_analysis/E-commerceRevenueDashboard)

---

# Deployment & Execution Guide

## Prerequisites
- **Docker & Docker Compose** — runs the PySpark containerized environment
- **Python 3.10+** — local pipeline orchestration
- **Git** — source control

---

## 1. Environment Initialization

```bash
# Clone the repository
git clone https://github.com/LeonDes7/ecom-analytics-pipeline.git

# Navigate into the project directory
cd ecom-analytics-pipeline

# Build the Docker image (includes PySpark + all dependencies)
docker-compose build
```

---

## 2. Run the Full Pipeline

Make sure Docker Desktop is running, then execute:

```bash
python run_pipeline.py
```

This single command runs all 10 pipeline steps automatically — from raw data extraction through dbt data quality testing.

### Under the Hood
- **01_download.py** — Downloads raw Excel dataset over HTTP
- **02_inspect_raw.py** — Profiles data volume, schema, and null completeness
- **03_clean_validate.py** — Pandas silver-level cleaning, exports clean CSV and raw CSV for Spark
- **spark_transform.py** — PySpark distributed cleaning inside Docker, writes partitioned Parquet
- **04_analytics_features.py** — Builds daily revenue, top product, and country revenue aggregates
- **07_export_parquet.py** — Exports cleaned transactions as columnar Parquet (pyarrow/snappy)
- **05_load_duckdb.py** — Bulk loads analytics CSVs into DuckDB OLAP warehouse with B-Tree indexes
- **06_run_sql.py** — Runs 6 analytical queries against DuckDB, outputs console previews
- **dbt run** — Compiles and executes 4 staging and mart SQL transformation models
- **dbt test** — Runs 9 automated data quality assertions across all tables

---

## 3. Verification

A successful run ends with:

```
🚀 FULL PIPELINE EXECUTED SUCCESSFULLY!
```

dbt test output:
```
Done. PASS=9 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=9
```

---

## 4. Run Individual Steps

To run analytical queries or dbt independently:

```bash
# SQL analytics against DuckDB
python python/06_run_sql.py

# dbt transformations only
cd dbt_project
dbt run --profiles-dir .
dbt test --profiles-dir .
```