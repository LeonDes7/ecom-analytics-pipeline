import pandas as pd

RAW_PATH = "data/raw/online_retail.xlsx"
CLEAN_PATH = "data/clean/online_retail_clean.csv"

# Load raw source data
df = pd.read_excel(RAW_PATH)
print("Raw shape:", df.shape)

# Data Quality Rule 1: Drop records missing primary business identifiers (CustomerID)
df = df.dropna(subset=["CustomerID"])

# Data Quality Rule 2: Filter out invoices starting with 'C' (removes cancellations/returns to isolate pure revenue)
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Data Quality Rule 3: Enforce business logic constraints (exclude zero or negative quantities and unit prices)
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Standardization: Strip whitespace and normalize string casing to guarantee clean categorical grouping
df["Country"] = df["Country"].str.strip().str.upper()
df["Description"] = df["Description"].str.strip()

# Schema Enforcement: Cast numeric identifiers to integer and parse text dates to standard datetime objects
df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Feature Engineering: Derive a new calculated metric column representing total transactional revenue
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Validation Phase: Print post-cleaning dimensions and confirm zero null values remain in critical columns
print("Clean shape:", df.shape)
print(df.isnull().sum())

# Persistence: Write the sanitized Silver-level dataset to a CSV file (without arbitrary pandas index columns)
df.to_csv(CLEAN_PATH, index=False)
print("Clean data saved to:", CLEAN_PATH)