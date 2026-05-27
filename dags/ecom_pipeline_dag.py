from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum

# Operational Guardrails: Define standard SLAs and retry mechanisms for distributed batch processing
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,       # Ensures task failures in previous runs don't block the current execution window
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,                  # Resilience mechanism to handle transient network or infrastructure blips
    'retry_delay': timedelta(minutes=5),
}

# Core DAG Definition
with DAG(
    'ecommerce_analytics_pipeline',
    default_args=default_args,
    description='End-to-end e-commerce ETL pipeline orchestrating PySpark ingestion and dbt warehouse modeling',
    schedule_interval='@daily',    # Batch processing interval grain
    start_date=pendulum.datetime(2026, 4, 19, tz="UTC"), # Timezone-aware execution anchor to prevent daylight savings shifts
    catchup=False,                 # Disables backfilling historical days to preserve compute resources on initialization
    tags=['ecommerce', 'bigquery', 'dbt'],
) as dag:

    # Global environment configuration parameterizing execution paths
    project_root = '/path/to/your/ecom-analytics-pipeline'

    # Task 1: Edge Ingestion Layer
    download_raw = BashOperator(
        task_id='download_raw_data',
        bash_command=f'python {project_root}/01_download.py',
    )

    # Task 2: Silver-Tier Sanitization Layer
    clean_validate = BashOperator(
        task_id='clean_and_validate',
        bash_command=f'python {project_root}/03_clean_validate.py',
    )

    # Task 3: Intermediate Storage Persistence (Staging Parquet assets)
    export_parquet = BashOperator(
        task_id='export_to_parquet',
        bash_command=f'python {project_root}/07_export_parquet.py',
    )

    # Task 4: Gold-Tier Data Warehouse Transformation & Automated Regression Testing
    run_dbt_models = BashOperator(
        task_id='run_dbt_transformations',
        # Executes incremental models and immediately runs data quality assertions within the same execution context
        bash_command=f'cd {project_root}/dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir .',
    )
    
    # Orchestration Dependency Graph Construction
    # Establishes an immutable, linear execution order enforcing strict upstream data lineage
    download_raw >> clean_validate >> export_parquet >> run_dbt_models