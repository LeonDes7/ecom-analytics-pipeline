# E-commerce Analytics Pipeline

An end-to-end e-commerce analytics pipeline built using **Python, SQL, SQLite/PostgreSQL, and Tableau**.  
This project demonstrates a realistic data engineering workflow: ingesting raw data, cleaning and validating it, creating analytical features, loading it into a database, and running analytical SQL queries for visualization.

---

##  Project Overview

The goal of this project is to simulate a real-world analytics pipeline for an e-commerce business.  
Raw transaction data is processed through a structured ETL pipeline and transformed into analytics-ready tables, which are then queried using SQL and visualized in Tableau.

This project is designed to showcase:
- Practical **ETL pipeline design**
- **Python-based data cleaning & transformation**
- **SQL analytics queries**
- **Database loading**
- **BI integration (Tableau)**

---

##  Tech Stack

- **Python** (pandas, sqlalchemy)
- **SQL** (analytical queries)
- **SQLite / PostgreSQL**
- **Tableau Public**
- **Git & GitHub**

---

##  Pipeline Workflow

### 1️ Data Ingestion
- Downloads raw e-commerce transaction data.
- Stores data locally for processing.

### 2️ Data Inspection
- Checks schema, row counts, missing values, and data types.
- Identifies potential quality issues early.

### 3️ Data Cleaning & Validation
- Removes invalid rows (null IDs, negative quantities, etc.)
- Standardizes fields (country names, dates)
- Deduplicates records

### 4️ Analytics Feature Engineering
- Computes revenue (`quantity × unit_price`)
- Creates daily revenue aggregates
- Prepares analytics-friendly tables

### 5️ Database Load
- Loads cleaned and transformed data into SQLite (or PostgreSQL).
- Tables are structured for analytical querying.

### 6️ SQL Analytics
- Runs analytical SQL queries to answer business questions:
  - Daily revenue trends
  - Top-selling products
  - Revenue by country
- Outputs are used directly in Tableau.

### 7️ Visualization
- Connects Tableau to the database.
- Builds an interactive dashboard for stakeholders.

---

##  Example Analytics Questions

- What is the total revenue per day?
- Which products generate the most revenue?
- Which countries contribute the most sales?
- How does revenue trend over time?

---

##  Tableau Dashboard

The final dashboard is published on **Tableau Public** and includes:
- Revenue over time
- Top products by revenue
- Revenue by country (map view)

 **Tableau Public Link:**  
 *([Tableau Dashboard](https://public.tableau.com/app/profile/xuan.zhang8153/viz/ecommerce_tableau_analysis/E-commerceRevenueDashboard))*







