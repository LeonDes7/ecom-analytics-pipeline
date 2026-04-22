WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
)

SELECT
    DATE(invoice_date) AS reporting_date,
    COUNT(DISTINCT invoice_id) AS total_orders,
    SUM(quantity) AS total_items_sold,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM transactions
GROUP BY 1
ORDER BY 1