import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parents[1]

CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = quote_plus(os.getenv("PG_PASSWORD", ""))
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "ecom")

if not PG_PASSWORD:
    raise ValueError("PG_PASSWORD is empty. Set it first: set PG_PASSWORD=your_password")

DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(DB_URL)

def main():
    transactions = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
    daily_revenue = pd.read_csv(ANALYTICS_DIR / "daily_revenue.csv")
    top_products = pd.read_csv(ANALYTICS_DIR / "top_products.csv")
    country_revenue = pd.read_csv(ANALYTICS_DIR / "country_revenue.csv")

    transactions.to_sql("transactions", engine, if_exists="replace", index=False)
    daily_revenue.to_sql("daily_revenue", engine, if_exists="replace", index=False)
    top_products.to_sql("top_products", engine, if_exists="replace", index=False)
    country_revenue.to_sql("country_revenue", engine, if_exists="replace", index=False)

    with engine.begin() as conn:
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_transactions_invoice ON transactions("InvoiceNo");'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions("CustomerID");'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions("InvoiceDate");'))

    print(" Loaded tables into PostgreSQL database:", PG_DB)

if __name__ == "__main__":
    main()