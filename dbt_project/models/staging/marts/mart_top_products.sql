WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
)

SELECT
    product_code,
    product_description,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue
FROM transactions
GROUP BY 1, 2
ORDER BY total_revenue DESC