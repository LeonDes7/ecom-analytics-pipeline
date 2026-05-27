import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/online_retail.xlsx")

def main():
    # Profiling Phase: Load raw dataset into memory to assess data quality and structural anomalies
    df = pd.read_excel(RAW_PATH)

    # Inspect data volume (matrix dimensions)
    print("Shape (rows, columns):")
    print(df.shape)
    
    # Check schema naming conventions
    print("\nColumns:")
    print(df.columns.tolist())

    # Preview data to identify implicit data types, formatting, and formatting errors
    print("\nFirst 5 rows:")
    print(df.head())

    # Quantify completeness by counting null values per attribute
    print("\nMissing values by column:")
    print(df.isna().sum())

    # Audit explicit data types assigned by the engine and assess memory usage
    print("\nBasic info:")
    print(df.info())

if __name__ == "__main__":
    main()