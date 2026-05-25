-- CUSTOMER KPIs: Top 10 Cities by Revenue
USE retail_warehouse;
GO

SELECT TOP 10
    dc.customer_city,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.payment_value) AS total_revenue,
    AVG(f.payment_value) AS average_order_value
FROM fact_orders f
JOIN dim_customers dc ON f.customer_key = dc.customer_key
WHERE f.order_status = 'delivered'
GROUP BY dc.customer_city
ORDER BY total_revenue DESC;
GO