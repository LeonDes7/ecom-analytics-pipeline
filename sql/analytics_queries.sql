-- 1) Total revenue + orders
SELECT
  COUNT(DISTINCT InvoiceNo) AS orders,
  SUM(TotalPrice) AS revenue
FROM transactions;

-- 2) Monthly revenue trend
SELECT
  strftime('%Y-%m', InvoiceDate) AS month,
  SUM(TotalPrice) AS revenue
FROM transactions
GROUP BY 1
ORDER BY 1;

-- 3) Top 10 customers by revenue
SELECT
  CustomerID,
  SUM(TotalPrice) AS revenue
FROM transactions
GROUP BY CustomerID
ORDER BY revenue DESC
LIMIT 10;

-- 4) Repeat customers (2+ distinct invoices)
SELECT
  CustomerID,
  COUNT(DISTINCT InvoiceNo) AS orders
FROM transactions
GROUP BY CustomerID
HAVING COUNT(DISTINCT InvoiceNo) >= 2
ORDER BY orders DESC;

-- 5) Top 10 products by revenue
SELECT
  StockCode,
  Description,
  SUM(Quantity) AS units_sold,
  SUM(TotalPrice) AS revenue
FROM transactions
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 10;

-- 6) Country revenue share (excluding UK if you want)
SELECT
  Country,
  SUM(TotalPrice) AS revenue
FROM transactions
GROUP BY Country
ORDER BY revenue DESC;