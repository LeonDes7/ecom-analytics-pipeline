import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/online_retail.xlsx")

def main():
    df = pd.read_excel(RAW_PATH)

    print("Shape (rows, columns):")
    print(df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values by column:")
    print(df.isna().sum())

    print("\nBasic info:")
    print(df.info())

if __name__ == "__main__":
    main()