USE retail_warehouse;
GO

CREATE TABLE dim_customers (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id NVARCHAR(50) NOT NULL,
    customer_unique_id NVARCHAR(50),
    customer_city NVARCHAR(100),
    customer_state NVARCHAR(5)
);

CREATE TABLE dim_products (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id NVARCHAR(50) NOT NULL,
    product_category_name_english NVARCHAR(100),
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2)
);

CREATE TABLE dim_sellers (
    seller_key INT IDENTITY(1,1) PRIMARY KEY,
    seller_id NVARCHAR(50) NOT NULL,
    seller_city NVARCHAR(100),
    seller_state NVARCHAR(5)
);

CREATE TABLE dim_time (
    time_key INT IDENTITY(1,1) PRIMARY KEY,
    order_purchase_timestamp DATETIME2,
    purchase_year INT,
    purchase_month INT,
    purchase_day INT,
    purchase_hour INT,
    day_of_week NVARCHAR(15),
    month_name NVARCHAR(15)
);

CREATE TABLE fact_orders (
    order_id NVARCHAR(50) NOT NULL,
    customer_key INT,
    product_key INT,
    seller_key INT,
    time_key INT,
    price DECIMAL(12, 2),
    freight_value DECIMAL(12, 2),
    payment_type NVARCHAR(30),
    payment_installments INT,
    payment_value DECIMAL(12, 2),
    review_score INT,
    order_status NVARCHAR(30),
    FOREIGN KEY (customer_key) REFERENCES dim_customers(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_products(product_key),
    FOREIGN KEY (seller_key) REFERENCES dim_sellers(seller_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);
GO