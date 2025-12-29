import pandas as pd

RAW_PATH = "data/raw/online_retail.xlsx"
CLEAN_PATH = "data/clean/online_retail_clean.csv"

# Load raw data
df = pd.read_excel(RAW_PATH)
print("Raw shape:", df.shape)

# Drop missing customer IDs
df = df.dropna(subset=["CustomerID"])

# Remove cancelled invoices
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove invalid quantities and prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Standardize text fields
df["Country"] = df["Country"].str.strip().str.upper()
df["Description"] = df["Description"].str.strip()

# Convert data types
df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Add derived metric
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Validation
print("Clean shape:", df.shape)
print(df.isnull().sum())

# Save clean data
df.to_csv(CLEAN_PATH, index=False)
print("Clean data saved to:", CLEAN_PATH)