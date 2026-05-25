-- PRODUCT KPIs: Top 10 Best-Selling Categories

USE retail_warehouse;
GO

SELECT TOP 10
    dp.product_category_name_english,
    COUNT(f.order_id) AS items_sold,
    SUM(f.price) AS total_product_revenue,
    AVG(f.review_score) AS avg_review_score
FROM fact_orders f
JOIN dim_products dp ON f.product_key = dp.product_key
WHERE f.order_status = 'delivered'
GROUP BY dp.product_category_name_english
ORDER BY total_product_revenue DESC;
GO