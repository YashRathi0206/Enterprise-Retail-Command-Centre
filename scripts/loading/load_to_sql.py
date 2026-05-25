import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from sqlalchemy import text
from config import OLIST_FILES, PATHS, DB_CONNECTION_STRING
from utils.logger import get_logger
from utils.db_connection import get_engine

logger = get_logger(__name__)

class DataLoader:
    def __init__(self):
        self.raw_path = Path(PATHS["raw_data"])
        self.engine = get_engine()

    def run(self):
        """Loads all raw CSVs into SQL Server staging tables."""
        logger.info("=" * 60)
        logger.info("STARTING DATA LOAD TO SQL SERVER")
        logger.info("=" * 60)

        # Dictionary mapping CSV names to their SQL Server table names
        table_mapping = {
            "customers": "stg_customers",
            "orders": "stg_orders",
            "order_items": "stg_order_items",
            "order_payments": "stg_order_payments",
            "order_reviews": "stg_order_reviews",
            "products": "stg_products",
            "sellers": "stg_sellers",
            "product_category_translation": "stg_product_category_translation",
        }

        for dataset_name, table_name in table_mapping.items():
            filename = OLIST_FILES[dataset_name]
            file_path = self.raw_path / filename
            
            if not file_path.exists():
                logger.warning(f"File not found: {filename}. Skipping.")
                continue

            try:
                # Step 1: Read the CSV
                df = pd.read_csv(file_path, encoding="utf-8")
                
                # Step 2: DATA CLEANING - Handle duplicates before loading
                if dataset_name == "order_reviews":
                    original_rows = len(df)
                    # Keep the first review, drop the duplicates
                    df = df.drop_duplicates(subset=['review_id'], keep='first')
                    dropped = original_rows - len(df)
                    if dropped > 0:
                        logger.info(f"  Cleaned: Removed {dropped} duplicate review_ids")

                # Step 3: Load to SQL Server
                # Using 'replace' so if you run this twice, it safely overwrites
                logger.info(f"Loading {dataset_name} into {table_name}...")
                df.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='replace', 
                    index=False
                )
                
                # Step 4: Verify row count
                with self.engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.fetchone()[0]
                
                logger.info(f"✓ Success: {table_name} now has {count:,} rows")

            except Exception as e:
                logger.error(f"✗ Failed to load {dataset_name}: {e}")

        self.engine.dispose()
        logger.info("=" * 60)
        logger.info("DATA LOAD COMPLETED")
        logger.info("=" * 60)

if __name__ == "__main__":
    loader = DataLoader()
    loader.run()