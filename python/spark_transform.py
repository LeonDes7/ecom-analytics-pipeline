from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

# Initialize SparkSession to enable distributed processing via the Catalyst Optimizer and Tungsten engine
spark = SparkSession.builder.appName("EcomAnalytics").getOrCreate()

source_path = "/opt/spark/project/data/raw/online_retail.csv"
output_path = "/opt/spark/project/data/warehouse/transactions_spark.parquet"

print("STEP 1: LOADING DATA...")
# Read raw CSV data, automatically parse header names, and infer schema types in a distributed pass
df = spark.read.csv(source_path, header=True, inferSchema=True)
print(f"ROWS FOUND: {df.count()}")

print("STEP 2: TRANSFORMING DATA...")
# Execute distributed row-level filtering to exclude invalid operational states (null IDs and negative/zero items)
cleaned_df = df.filter(col("CustomerID").isNotNull()) \
               .filter(col("Quantity") > 0)

print("STEP 3: ATTEMPTING WRITE TO WAREHOUSE...")
# Save data utilizing overwrite mode to ensure idempotency (rerunning the pipeline safely replaces old files)
# Persist using Parquet format for highly efficient, compressed columnar storage
cleaned_df.write.mode("overwrite").parquet(output_path)

if os.path.exists(output_path):
    print(f"STEP 4: SUCCESS! Data written to {output_path}")
    print(f"FINAL RECORD COUNT: {cleaned_df.count()}")
else:
    print("STEP 4: WRITE FAILED. Folder not found.")

# Gracefully shut down the Spark context and release distributed executor resources
spark.stop()