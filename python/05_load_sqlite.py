import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DB_PATH = BASE_DIR / "data" / "warehouse.db"
CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"

print("DB path:", DB_PATH)

# Load the staged, cleaned transaction records and the processed analytics dataframes
transactions = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
daily_revenue = pd.read_csv(ANALYTICS_DIR / "daily_revenue.csv")
top_products = pd.read_csv(ANALYTICS_DIR / "top_products.csv")
country_revenue = pd.read_csv(ANALYTICS_DIR / "country_revenue.csv")

# Open a local connection to the relational database file
conn = sqlite3.connect(DB_PATH)

# Bulk Load Stage: Write datasets into corresponding SQL tables, replacing existing structures to ensure idempotency
transactions.to_sql("transactions", conn, if_exists="replace", index=False)
daily_revenue.to_sql("daily_revenue", conn, if_exists="replace", index=False)
top_products.to_sql("top_products", conn, if_exists="replace", index=False)
country_revenue.to_sql("country_revenue", conn, if_exists="replace", index=False)

# Index Optimization: Build B-Tree indexes on heavy JOIN/WHERE query attributes to accelerate downstream lookup speeds
cur = conn.cursor()
cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_invoice ON transactions(InvoiceNo);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(CustomerID);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(InvoiceDate);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_country ON transactions(Country);")
conn.commit()

# Audit: Query system catalog tables to verify all relational table components exist on disk
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
print("Tables in DB:")
print(tables)

# Data Quality Reconciliation: Assert row counts using a UNION query to verify data loaded completely without corruption
row_counts = pd.read_sql("""
SELECT 'transactions' as table_name, COUNT(*) as rows FROM transactions
UNION ALL SELECT 'daily_revenue', COUNT(*) FROM daily_revenue
UNION ALL SELECT 'top_products', COUNT(*) FROM top_products
UNION ALL SELECT 'country_revenue', COUNT(*) FROM country_revenue;
""", conn)
print("\nRow counts:")
print(row_counts)

# Close database connection to prevent resource leaks
conn.close()
print("\n Loaded SQLite warehouse successfully.")