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

# Deployment & Execution Guide

This guide walks you through setting up the infrastructure, executing the data pipelines, running analytical queries, and validating data quality constraints.

---

## Prerequisites

Before initialization, ensure your local development environment has the following software installed:
* **Docker & Docker Compose:** For infrastructure containerization and isolated dependency management.
* **Python 3.10+:** Required for local pipeline orchestration scripts.
* **Git:** For source control and repository management.

---

## 1. Environment Initialization

Clone the remote repository, navigate to the project root directory, and spin up the containerized infrastructure (including the PySpark environment, DuckDB volume mappings, and dbt core modules) in detached mode.

```bash
# Clone the repository
git clone https://github.com/LeonDes7/ecom-analytics-pipeline.git

# Navigate into the project directory
cd ecom-analytics-pipeline

# Build and start containerized resources in the background
docker-compose up -d
```
*> Note: The `-d` flag runs the containers in detached mode, leaving your active terminal shell open.*

---

## 2. Core ETL Pipeline Execution

Execute the core Python orchestration script. This handles the end-to-end flow of raw data ingestion, distributed PySpark cleaning, storage persistence optimization, and loading into the OLAP warehouse layer.

```bash
# Run the orchestration script to execute ingestion, silver sanitization, and warehousing
python run_pipeline.py
```

### Under the Hood
* **01_download.py & 02_inspect_raw.py:** Downloads the raw transactional dataset over HTTP and profiles the data volume, columns, and completeness.
* **03_clean_validate.py / spark_transform.py:** Executes row-level cleaning (drops null customer IDs, filters out negative/zero quantities, isolates cancellations) using PySpark distributed processing.
* **04_analytics_features.py & 07_export_parquet.py:** Derives new business metrics (e.g., total price) and exports the data into highly compressed, columnar Apache Parquet files.
* **05_load_sqlite.py:** Connects to the database and performs a batch bulk-load while building optimized B-Tree indexes on heavy `JOIN` and `WHERE` lookup keys.

---

## 3. Warehouse Transformations & Data Quality Testing

Navigate into the analytics directory to compile your SQL transformation models, generate business-ready data marts, and trigger automated regression testing.

```bash
# Move into the dbt project context
cd dbt_project

# Compile and execute modular staging and mart SQL transformation models
dbt run --profiles-dir .

# Execute the 7 automated data quality assertions (uniqueness and non-null constraints)
dbt test --profiles-dir .
```

### Verification
A successful deployment will return the following status block in your terminal view:
```text
Passed: 7
Failed: 0
Error: 0
```
This confirms all source data integrity guardrails have passed, and clean, reliable datasets are fully prepared for visualization in downstream Tableau dashboards.

---

## 4. Analytical Verification

To verify the warehouse data layout and inspect aggregated metrics without entering a GUI tool, execute the analytical query script:

```bash
# Return to the root project directory if needed, then run the query inspector
python python/06_run_sql.py
```
This parses your analytical SQL script files, runs queries against the active database instance, and outputs console previews of top products, daily revenue totals, and geographic performance summaries.
