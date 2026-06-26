import subprocess
import os
import sys

def run_command(step_name, command, cwd=None):
    print(f"\n{'='*10} STARTING: {step_name} {'='*10}")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd)
        print(f"SUCCESS: {step_name} completed.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {step_name} failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    dbt_path = os.path.join(base_path, "dbt_project")

    # Step 1: Extract — Download raw Excel dataset
    run_command("Data Extraction", "python python/01_download.py")

    # Step 2: Inspect — Profile raw data quality and schema
    run_command("Raw Data Inspection", "python python/02_inspect_raw.py")

    # Step 3: Clean & Validate — pandas silver-level cleaning, saves clean CSV + raw CSV for Spark
    run_command("Data Cleaning & Validation", "python python/03_clean_validate.py")

    # Step 4: PySpark Distributed Transform — runs inside Docker (Linux, no winutils needed)
    run_command(
        "PySpark Distributed Transform",
        'docker-compose run --remove-orphans spark-master bash -c "python3 /opt/spark/project/python/spark_transform.py"'
    )

    # Step 5: Analytics Feature Engineering — build daily/product/country aggregates
    run_command("Analytics Feature Engineering", "python python/04_analytics_features.py")

    # Step 6: Export Parquet — pandas Parquet export for warehouse backup layer
    run_command("Parquet Export", "python python/07_export_parquet.py")

    # Step 7: Load DuckDB — bulk load analytics CSVs into DuckDB OLAP warehouse
    run_command("DuckDB Warehouse Load", "python python/05_load_duckdb.py")

    # Step 8: SQL Analytics — run analytical queries against DuckDB
    run_command("SQL Analytics", "python python/06_run_sql.py")

    # Step 9: dbt Transformations — build staging and mart models on Spark Parquet output
    run_command("dbt Analytics Transformations", "dbt run --profiles-dir .", cwd=dbt_path)

    # Step 10: dbt Tests — run 8 automated data quality assertions
    run_command("Data Quality Testing", "dbt test --profiles-dir .", cwd=dbt_path)

    print("\n" + "="*35)
    print("FULL PIPELINE EXECUTED SUCCESSFULLY!")
    print("="*35)