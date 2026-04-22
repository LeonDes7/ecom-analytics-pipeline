import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"

# Our local "data warehouse" folder
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"
PARQUET_PATH = WAREHOUSE_DIR / "transactions_raw.parquet"

def main():
    # 1. Load clean data
    df = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
    
    # 2. Ensure warehouse directory exists
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 3. Write to Parquet
    df.to_parquet(PARQUET_PATH, engine="pyarrow", index=False)
    print(f"Successfully exported schema-enforced Parquet file to: {PARQUET_PATH}")

if __name__ == "__main__":
    main()