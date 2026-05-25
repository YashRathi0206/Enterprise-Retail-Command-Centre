-- ENTERPRISE RETAIL INTELLIGENCE COMMAND CENTRE
-- SQL Server Database & Staging Schema Creation

-- 1. Create the main database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'retail_warehouse')
BEGIN
    CREATE DATABASE retail_warehouse;
END
GO

-- 2. Tell SQL Server we are working inside this database
USE retail_warehouse;
GO

-- 3. Create Staging Tables (The "Mailroom")
-- Notice we use NVARCHAR for text to support international characters (like São Paulo)

CREATE TABLE stg_customers (
    customer_id NVARCHAR(50) NOT NULL,
    customer_unique_id NVARCHAR(50) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city NVARCHAR(100),
    customer_state NVARCHAR(5),
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (customer_id)
);

CREATE TABLE stg_orders (
    order_id NVARCHAR(50) NOT NULL,
    customer_id NVARCHAR(50),
    order_status NVARCHAR(30),
    order_purchase_timestamp DATETIME2,
    order_approved_at DATETIME2,
    order_delivered_carrier_date DATETIME2,
    order_delivered_customer_date DATETIME2,
    order_estimated_delivery_date DATETIME2,
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (order_id)
);

CREATE TABLE stg_order_items (
    order_id NVARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    product_id NVARCHAR(50),
    seller_id NVARCHAR(50),
    shipping_limit_date DATETIME2,
    price DECIMAL(12, 2),
    freight_value DECIMAL(12, 2),
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE stg_order_payments (
    order_id NVARCHAR(50) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type NVARCHAR(30),
    payment_installments INT,
    payment_value DECIMAL(12, 2),
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE stg_order_reviews (
    review_id NVARCHAR(50) NOT NULL,
    order_id NVARCHAR(50),
    review_score INT,
    review_comment_title NVARCHAR(MAX),
    review_comment_message NVARCHAR(MAX),
    review_creation_date DATETIME2,
    review_answer_timestamp DATETIME2,
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (review_id)
);

CREATE TABLE stg_products (
    product_id NVARCHAR(50) NOT NULL,
    product_category_name NVARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(12, 2),
    product_length_cm DECIMAL(10, 2),
    product_height_cm DECIMAL(10, 2),
    product_width_cm DECIMAL(10, 2),
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (product_id)
);

CREATE TABLE stg_sellers (
    seller_id NVARCHAR(50) NOT NULL,
    seller_zip_code_prefix INT,
    seller_city NVARCHAR(100),
    seller_state NVARCHAR(5),
    _ingested_at DATETIME2,
    _source_file NVARCHAR(100),
    PRIMARY KEY (seller_id)
);
GO