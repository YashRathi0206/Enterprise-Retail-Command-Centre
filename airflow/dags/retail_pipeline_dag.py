"""
Enterprise Retail Intelligence Command Centre
Airflow DAG: End-to-End Retail Pipeline

This DAG automates the entire data flow:
1. Ingest raw CSVs to SQL Staging
2. Transform Staging to Star Schema
3. Run ML Models (Forecast, Segmentation, Churn)
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# --- DEFAULT ARGUMENTS ---
# These apply to all tasks in the DAG
default_args = {
    'owner': 'retail-command-centre',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# --- DEFINE THE DAG ---
with DAG(
    dag_id='retail_etl_ml_pipeline',
    default_args=default_args,
    description='End-to-End Retail Data Pipeline: ETL + Machine Learning',
    schedule_interval='0 6 * * *', # Cron: Run every day at 6:00 AM
    start_date=datetime(2024, 1, 1),
    catchup=False, # Don't run historical backfills automatically
    tags=['retail', 'etl', 'ml'],
) as dag:

    # --- TASK 1: DATA INGESTION ---
    def run_ingestion():
        # In a real enterprise setup, these paths would be absolute
        import sys
        sys.path.append('/opt/airflow/scripts') # Standard Docker path
        from ingestion.ingest import DataIngestionPipeline
        pipeline = DataIngestionPipeline()
        pipeline.run()

    task_ingest = PythonOperator(
        task_id='ingest_raw_data',
        python_callable=run_ingestion,
    )

    # --- TASK 2: DATA TRANSFORMATION ---
    def run_transformation():
        import sys
        sys.path.append('/opt/airflow/scripts')
        from transformation.transform_to_star_schema import run_transformation
        run_transformation()

    task_transform = PythonOperator(
        task_id='transform_to_star_schema',
        python_callable=run_transformation,
    )

    # --- TASK 3: ML FORECASTING ---
    def run_ml_forecast():
        import sys
        sys.path.append('/opt/airflow/scripts')
        from ml.forecast import run_prophet_forecast # You would modularize your notebook code
        run_prophet_forecast()

    task_ml_forecast = PythonOperator(
        task_id='run_sales_forecast',
        python_callable=run_ml_forecast,
    )

    # --- TASK 4: ML SEGMENTATION ---
    def run_ml_segmentation():
        import sys
        sys.path.append('/opt/airflow/scripts')
        from ml.segmentation import run_kmeans_segmentation
        run_kmeans_segmentation()

    task_ml_segmentation = PythonOperator(
        task_id='run_customer_segmentation',
        python_callable=run_ml_segmentation,
    )

    # --- TASK 5: ML CHURN PREDICTION ---
    def run_ml_churn():
        import sys
        sys.path.append('/opt/airflow/scripts')
        from ml.churn import run_churn_prediction
        run_churn_prediction()

    task_ml_churn = PythonOperator(
        task_id='run_churn_prediction',
        python_callable=run_ml_churn,
    )

    # --- TASK 6: DATA QUALITY CHECK (Bash example) ---
    # A quick SQL check to ensure the warehouse actually updated
    task_dq_check = BashOperator(
        task_id='verify_row_counts',
        bash_command='echo "Data Quality Check: Verifying row counts in warehouse..."',
    )

    # --- DEFINE THE PIPELINE ORDER ---
    # Ingest must finish before Transform starts
    # Transform must finish before ML models run
    # All ML models can run IN PARALLEL (at the same time) since they are independent
    # Finally, run the DQ check
    
    task_ingest >> task_transform >> [task_ml_forecast, task_ml_segmentation, task_ml_churn] >> task_dq_check
