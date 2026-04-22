WITH source AS (
    SELECT * FROM read_parquet('../data/warehouse/transactions_spark.parquet/*.parquet')
),

renamed AS (
    SELECT
        CAST("InvoiceNo" AS VARCHAR) AS invoice_id,
        CAST("StockCode" AS VARCHAR) AS product_code,
        "Description" AS product_description,
        CAST("Quantity" AS INT) AS quantity,
        -- Use strptime to handle the "12/1/2010" format
        strptime("InvoiceDate", '%m/%d/%Y %H:%M') AS invoice_date,
        CAST("UnitPrice" AS NUMERIC) AS unit_price,
        CAST("CustomerID" AS INT) AS customer_id,
        "Country" AS country,
        (CAST("Quantity" AS INT) * CAST("UnitPrice" AS NUMERIC)) AS revenue
    FROM source
    WHERE "Quantity" > 0 AND "UnitPrice" > 0
)

SELECT * FROM renamed