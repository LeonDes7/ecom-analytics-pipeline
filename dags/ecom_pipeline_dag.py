from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum  # <-- 1. Import pendulum instead of datetime

# Define pipeline default arguments
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'ecommerce_analytics_pipeline',
    default_args=default_args,
    description='End-to-end e-commerce ETL pipeline',
    schedule_interval='@daily',
    # 2. Use pendulum with an explicit timezone (UTC is standard)
    start_date=pendulum.datetime(2026, 4, 19, tz="UTC"), 
    catchup=False,
    tags=['ecommerce', 'bigquery', 'dbt'],
) as dag:

    # Define the project root path for the Bash commands
    # UPDATE THIS to your actual local repository path!
    project_root = '/path/to/your/ecom-analytics-pipeline'

    # Task 1: Ingestion
    download_raw = BashOperator(
        task_id='download_raw_data',
        bash_command=f'python {project_root}/01_download.py',
    )

    # Task 2: Cleaning
    clean_validate = BashOperator(
        task_id='clean_and_validate',
        bash_command=f'python {project_root}/03_clean_validate.py',
    )

    # Task 3: Load to Data Lake (Parquet format for DuckDB)
    export_parquet = BashOperator(
        task_id='export_to_parquet',
        bash_command=f'python {project_root}/07_export_parquet.py',
    )

    # And update the dependencies at the bottom:
    download_raw >> clean_validate >> export_parquet >> run_dbt_models

    # Task 4: dbt Transformation
    run_dbt_models = BashOperator(
        task_id='run_dbt_transformations',
        # Added --profiles-dir . so dbt looks in the current folder for the profile
        bash_command=f'cd {project_root}/dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir .',
    )
    
    # Set dependencies (This is the magic that runs them in order)
    download_raw >> clean_validate >> load_bigquery >> run_dbt_mode