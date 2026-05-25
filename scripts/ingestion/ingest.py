import pandas as pd
from pathlib import Path
from datetime import datetime

from config import OLIST_FILES, PATHS
from utils.logger import get_logger

logger = get_logger(__name__)

class DataIngestionPipeline:
    def __init__(self):
        self.raw_path = Path(PATHS["raw_data"])
        self.processed_path = Path(PATHS["processed_data"])
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.datasets = {}

    def run(self):
        """Runs the ingestion process for all CSV files."""
        logger.info("=" * 60)
        logger.info("STARTING DATA INGESTION PIPELINE")
        logger.info("=" * 60)

        for dataset_name, filename in OLIST_FILES.items():
            file_path = self.raw_path / filename
            
            if not file_path.exists():
                logger.warning(f"File not found: {filename}. Skipping.")
                continue

            # Step 1: Read CSV
            df = pd.read_csv(file_path, encoding="utf-8")
            
            # Step 2: Quality Checks
            rows, cols = df.shape
            nulls = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()
            
            logger.info(f"Loaded {filename}: {rows:,} rows | {cols} cols | {nulls} nulls | {duplicates} duplicates")
            
            # Step 3: Add Metadata (Audit trail - crucial for enterprise)
            df["_ingested_at"] = datetime.now()
            df["_source_file"] = filename
            
            # Step 4: Save to processed folder
            output_path = self.processed_path / filename
            df.to_csv(output_path, index=False)
            
            # Keep in memory for Phase 2
            self.datasets[dataset_name] = df

        logger.info("=" * 60)
        logger.info("DATA INGESTION PIPELINE COMPLETED")
        logger.info("=" * 60)
        return self.datasets

if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run()