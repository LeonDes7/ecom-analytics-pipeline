from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pathlib import Path
import os

# Detect whether running inside Docker or locally
# Docker sets the project at /opt/spark/project; locally we resolve from this file
IN_DOCKER = os.path.exists("/opt/spark/project")

if IN_DOCKER:
    BASE_DIR = Path("/opt/spark/project")
else:
    BASE_DIR = Path(__file__).resolve().parents[1]

SOURCE_PATH = str(BASE_DIR / "data" / "raw" / "online_retail.csv")
OUTPUT_PATH = str(BASE_DIR / "data" / "warehouse" / "transactions_spark.parquet")

# Initialize SparkSession — uses local mode when running outside Docker
spark = SparkSession.builder \
    .appName("EcomAnalytics") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("STEP 1: LOADING DATA...")
df = spark.read.csv(SOURCE_PATH, header=True, inferSchema=True)
print(f"ROWS FOUND: {df.count()}")

print("STEP 2: TRANSFORMING DATA...")
cleaned_df = df.filter(col("CustomerID").isNotNull()) \
               .filter(col("Quantity") > 0) \
               .filter(col("UnitPrice") > 0)

print("STEP 3: WRITING TO WAREHOUSE...")
# Write as partitioned Parquet — columnar, compressed, dbt-ready
cleaned_df.write.mode("overwrite").parquet(OUTPUT_PATH)
print(f"Data written to {OUTPUT_PATH}")
print(f"FINAL RECORD COUNT: {cleaned_df.count()}")

spark.stop()
