-- REVENUE KPIs: Monthly Revenue and Month-over-Month Growth
USE retail_warehouse;
GO

WITH MonthlyRevenue AS (
    -- Step 1: Calculate total revenue per month
    SELECT 
        dt.purchase_year,
        dt.month_name,
        SUM(f.payment_value) AS total_revenue,
        COUNT(DISTINCT f.order_id) AS total_orders
    FROM fact_orders f
    JOIN dim_time dt ON f.time_key = dt.time_key
    WHERE f.order_status = 'delivered'
    GROUP BY dt.purchase_year, dt.month_name
),
RevenueWithGrowth AS (
    -- Step 2: Use LAG window function to get previous month's revenue
    SELECT 
        purchase_year,
        month_name,
        total_revenue,
        total_orders,
        LAG(total_revenue, 1) OVER (ORDER BY purchase_year, month_name) AS prev_month_revenue
    FROM MonthlyRevenue
)
-- Step 3: Calculate the Growth Rate
SELECT 
    purchase_year,
    month_name,
    total_revenue,
    total_orders,
    prev_month_revenue,
    CAST(((total_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100 AS DECIMAL(10,2)) AS growth_rate_pct
FROM RevenueWithGrowth
ORDER BY purchase_year, month_name;
GO