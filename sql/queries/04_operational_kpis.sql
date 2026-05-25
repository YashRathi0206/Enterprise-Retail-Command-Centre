-- OPERATIONAL KPIs: Average Delivery Time in Days

USE retail_warehouse;
GO

SELECT 
    YEAR(order_purchase_timestamp) AS purchase_year,
    COUNT(order_id) AS delivered_orders,
    AVG(DATEDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)) AS avg_delivery_days,
    MAX(DATEDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)) AS max_delivery_days
FROM stg_orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
GROUP BY YEAR(order_purchase_timestamp)
ORDER BY purchase_year;
GO