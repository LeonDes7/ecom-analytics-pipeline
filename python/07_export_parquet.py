import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"

# Target local folder representing an immutable data lake/warehouse tier
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"
PARQUET_PATH = WAREHOUSE_DIR / "transactions_raw.parquet"

def main():
    # 1. Load clean transactional CSV
    df = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
    
    # 2. Ensure target path infrastructure exists
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 3. Export to Parquet utilizing the Apache Arrow engine
    # This enforces binary schemas, column metadata tracking, and high performance data compression (Snappy)
    df.to_parquet(PARQUET_PATH, engine="pyarrow", index=False)
    print(f"Successfully exported schema-enforced Parquet file to: {PARQUET_PATH}")

if __name__ == "__main__":
    main()