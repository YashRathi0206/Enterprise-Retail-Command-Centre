import os
from dotenv import load_dotenv

# Load the secrets from the .env file
load_dotenv()

# Database connection details for Microsoft SQL Server
DB_CONFIG = {
    "server": os.getenv("DB_SERVER", "localhost"), # localhost means your own computer
    "database": os.getenv("DB_NAME", "retail_warehouse"),
    "driver": "ODBC Driver 18 for SQL Server", # The translator we just downloaded
}

# SQLAlchemy connection string specifically for SQL Server Windows Authentication
# Trusted_Connection=yes means it uses your Windows login automatically!
DB_CONNECTION_STRING = (
    f"mssql+pyodbc://@{DB_CONFIG['server']}/{DB_CONFIG['database']}"
    f"?driver={DB_CONFIG['driver']}"
    f"&TrustServerCertificate=yes" # Prevents certificate errors on local machines
    f"&Trusted_Connection=yes"
)

# File paths
PATHS = {
    "raw_data": os.getenv("RAW_DATA_PATH", "./data/raw"),
    "processed_data": os.getenv("PROCESSED_DATA_PATH", "./data/processed"),
}

# The exact filenames from Kaggle
OLIST_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
}