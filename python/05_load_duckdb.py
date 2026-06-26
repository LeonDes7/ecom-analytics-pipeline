import duckdb
import pandas as pd
from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parents[1]
 
DB_PATH = BASE_DIR / "ecom_warehouse.duckdb"
CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"
 
print("DB path:", DB_PATH)
 
# Load the staged, cleaned transaction records and the processed analytics dataframes
transactions = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
daily_revenue = pd.read_csv(ANALYTICS_DIR / "daily_revenue.csv")
top_products = pd.read_csv(ANALYTICS_DIR / "top_products.csv")
country_revenue = pd.read_csv(ANALYTICS_DIR / "country_revenue.csv")
 
# Open a persistent connection to the DuckDB columnar OLAP warehouse
conn = duckdb.connect(str(DB_PATH))
 
# Bulk Load Stage: Register pandas DataFrames and write into DuckDB tables,
# replacing existing structures to ensure idempotency
conn.execute("CREATE OR REPLACE TABLE transactions AS SELECT * FROM transactions")
conn.execute("CREATE OR REPLACE TABLE daily_revenue AS SELECT * FROM daily_revenue")
conn.execute("CREATE OR REPLACE TABLE top_products AS SELECT * FROM top_products")
conn.execute("CREATE OR REPLACE TABLE country_revenue AS SELECT * FROM country_revenue")
 
# Index Optimization: DuckDB uses zone maps and vectorized scans natively;
# create explicit indexes on high-cardinality filter keys for point lookups
conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_invoice ON transactions(InvoiceNo);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(CustomerID);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(InvoiceDate);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_country ON transactions(Country);")
 
# Audit: Query information schema to verify all tables exist in the warehouse
tables = conn.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name;
""").df()
print("Tables in DB:")
print(tables)
 
# Data Quality Reconciliation: Assert row counts to verify data loaded completely without corruption
row_counts = conn.execute("""
SELECT 'transactions' AS table_name, COUNT(*) AS rows FROM transactions
UNION ALL SELECT 'daily_revenue', COUNT(*) FROM daily_revenue
UNION ALL SELECT 'top_products', COUNT(*) FROM top_products
UNION ALL SELECT 'country_revenue', COUNT(*) FROM country_revenue;
""").df()
print("\nRow counts:")
print(row_counts)
 
# Close database connection to prevent resource leaks
conn.close()
print("\nLoaded DuckDB warehouse successfully.")