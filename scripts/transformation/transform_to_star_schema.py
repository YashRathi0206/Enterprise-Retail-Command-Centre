import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from sqlalchemy import text
from config import DB_CONNECTION_STRING
from utils.logger import get_logger
from utils.db_connection import get_engine

logger = get_logger(__name__)

def run_transformation():
    logger.info("=" * 60)
    logger.info("STARTING STAR SCHEMA TRANSFORMATION")
    logger.info("=" * 60)
    
    engine = get_engine()

    # ==========================================
    # 1. DIM_CUSTOMERS
    # ==========================================
    logger.info("Transforming dim_customers...")
    dim_customers = pd.read_sql("SELECT customer_id, customer_unique_id, customer_city, customer_state FROM stg_customers", engine)
    dim_customers.to_sql("dim_customers", engine, if_exists='append', index=False)
    logger.info("✓ dim_customers loaded.")

    # ==========================================
    # 2. DIM_PRODUCTS (Translating Portuguese to English)
    # ==========================================
    logger.info("Transforming dim_products...")
    # Left Join ensures we keep products even if they don't have a translation
    query = """
    SELECT 
        p.product_id, 
        ISNULL(t.product_category_name_english, p.product_category_name) AS product_category_name_english,
        p.product_weight_g, p.product_length_cm, p.product_height_cm, p.product_width_cm
    FROM stg_products p
    LEFT JOIN stg_product_category_translation t 
        ON p.product_category_name = t.product_category_name
    """
    dim_products = pd.read_sql(query, engine)
    dim_products.to_sql("dim_products", engine, if_exists='append', index=False)
    logger.info("✓ dim_products loaded.")

    # ==========================================
    # 3. DIM_SELLERS
    # ==========================================
    logger.info("Transforming dim_sellers...")
    dim_sellers = pd.read_sql("SELECT seller_id, seller_city, seller_state FROM stg_sellers", engine)
    dim_sellers.to_sql("dim_sellers", engine, if_exists='append', index=False)
    logger.info("✓ dim_sellers loaded.")

    # ==========================================
    # 4. DIM_TIME (Generating from order timestamps)
    # ==========================================
    logger.info("Transforming dim_time...")
    orders = pd.read_sql("SELECT order_id, order_purchase_timestamp FROM stg_orders", engine)
    
    time_df = orders[['order_purchase_timestamp']].copy()
    time_df['order_purchase_timestamp'] = pd.to_datetime(time_df['order_purchase_timestamp'])
    time_df['purchase_year'] = time_df['order_purchase_timestamp'].dt.year
    time_df['purchase_month'] = time_df['order_purchase_timestamp'].dt.month
    time_df['purchase_day'] = time_df['order_purchase_timestamp'].dt.day
    time_df['purchase_hour'] = time_df['order_purchase_timestamp'].dt.hour
    time_df['day_of_week'] = time_df['order_purchase_timestamp'].dt.day_name()
    time_df['month_name'] = time_df['order_purchase_timestamp'].dt.month_name()
    
    # Drop duplicate timestamps to keep the time table small and fast
    time_df = time_df.drop_duplicates(subset=['order_purchase_timestamp'])
    time_df.to_sql("dim_time", engine, if_exists='append', index=False)
    logger.info("✓ dim_time loaded.")

    # ==========================================
    # 5. FACT_ORDERS (Joining everything together)
    # ==========================================
    logger.info("Transforming fact_orders (This may take a moment)...")
    fact_query = """
    SELECT 
        o.order_id,
        dc.customer_key,
        dp.product_key,
        ds.seller_key,
        dt.time_key,
        i.price,
        i.freight_value,
        pay.payment_type,
        pay.payment_installments,
        pay.payment_value,
        r.review_score,
        o.order_status
    FROM stg_orders o
    JOIN stg_order_items i ON o.order_id = i.order_id
    JOIN stg_order_payments pay ON o.order_id = pay.order_id
    LEFT JOIN stg_order_reviews r ON o.order_id = r.order_id
    JOIN dim_customers dc ON o.customer_id = dc.customer_id
    JOIN dim_products dp ON i.product_id = dp.product_id
    JOIN dim_sellers ds ON i.seller_id = ds.seller_id
    JOIN dim_time dt ON o.order_purchase_timestamp = dt.order_purchase_timestamp
    """
    fact_orders = pd.read_sql(fact_query, engine)
    fact_orders.to_sql("fact_orders", engine, if_exists='append', index=False)
    logger.info("✓ fact_orders loaded.")

    engine.dispose()
    logger.info("=" * 60)
    logger.info("STAR SCHEMA TRANSFORMATION COMPLETED")
    logger.info("=" * 60)

if __name__ == "__main__":
    run_transformation()