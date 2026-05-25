from sqlalchemy import create_engine, text
from utils.logger import get_logger
from config import DB_CONNECTION_STRING

logger = get_logger(__name__)

def get_engine():
    """Creates the database engine for SQL Server."""
    try:
        # fast_executemany=True is CRITICAL for fast inserts into SQL Server
        engine = create_engine(DB_CONNECTION_STRING, fast_executemany=True)
        return engine
    except Exception as e:
        logger.error(f"Database engine failed: {e}")
        raise

def test_connection() -> bool:
    """Tests if Python can talk to SQL Server."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        logger.info("SQL Server connection test: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"SQL Server connection test: FAILED — {e}")
        return False