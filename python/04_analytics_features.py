import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

CLEAN_PATH = BASE_DIR / "data" / "clean" / "online_retail_clean.csv"
OUT_DIR = BASE_DIR / "data" / "analytics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load clean data
df = pd.read_csv(CLEAN_PATH, parse_dates=["InvoiceDate"])
print("Loaded clean shape:", df.shape)

# Add a Date column for grouping
df["Date"] = df["InvoiceDate"].dt.date

# 1) Daily revenue metrics
daily = (
    df.groupby("Date")
      .agg(
          orders=("InvoiceNo", "nunique"),
          items_sold=("Quantity", "sum"),
          revenue=("TotalPrice", "sum"),
          unique_customers=("CustomerID", "nunique"),
      )
      .reset_index()
      .sort_values("Date")
)

daily_path = OUT_DIR / "daily_revenue.csv"
daily.to_csv(daily_path, index=False)
print("Saved:", daily_path)

# 2) Top products
top_products = (
    df.groupby(["StockCode", "Description"])
      .agg(
          units_sold=("Quantity", "sum"),
          revenue=("TotalPrice", "sum"),
      )
      .reset_index()
      .sort_values(["revenue", "units_sold"], ascending=False)
      .head(50)
)

top_products_path = OUT_DIR / "top_products.csv"
top_products.to_csv(top_products_path, index=False)
print("Saved:", top_products_path)

# 3) Country revenue
country = (
    df.groupby("Country")
      .agg(
          orders=("InvoiceNo", "nunique"),
          customers=("CustomerID", "nunique"),
          revenue=("TotalPrice", "sum"),
      )
      .reset_index()
      .sort_values("revenue", ascending=False)
)

country_path = OUT_DIR / "country_revenue.csv"
country.to_csv(country_path, index=False)
print("Saved:", country_path)

print("\nDaily (head):")
print(daily.head(5))

print("\nTop products (head):")
print(top_products.head(5))

print("\nCountry revenue (head):")
print(country.head(10))