WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
)

SELECT
    country,
    COUNT(DISTINCT invoice_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue
FROM transactions
GROUP BY 1
ORDER BY total_revenue DESC