import pandas as pd
import pandas_gbq
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"

# Configure Google Cloud Platform environment variables and schema destinations
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
DATASET_ID = "ecom_analytics"
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.transactions_raw"

def main():
    # 1. Load data
    df = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
    
    # 2. Local Staging Simulation: Write data to an immutable Parquet snapshot file
    # This mirrors standard production architectures where data stages in cloud storage (like GCS or AWS S3) before warehouse loading
    parquet_path = BASE_DIR / "data" / "clean" / "transactions.parquet"
    df.to_parquet(parquet_path, engine="pyarrow", index=False)
    print(f"Saved schema-enforced Parquet file to: {parquet_path}")

    # 3. Cloud Load: Push the structured data directly into a BigQuery enterprise analytical data warehouse table
    print(f"Uploading to BigQuery table: {TABLE_ID}...")
    pandas_gbq.to_gbq(
        df, 
        destination_table=TABLE_ID, 
        project_id=PROJECT_ID, 
        if_exists="replace"  # Replaces existing data partitions to maintain structural idempotency
    )
    print("Successfully loaded to BigQuery.")

if __name__ == "__main__":
    main()