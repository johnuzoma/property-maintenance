from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import boto3
import io
import pandas as pd
import os
from sqlalchemy import create_engine

@dag(
    schedule=None, 
    start_date=datetime(2025, 4, 9), 
    catchup=False, 
    tags=["minio", "postgres", "pandas"]
)
def load_property_maintenance_data():

    @task(execution_timeout=timedelta(minutes=10), retries=2, retry_delay=timedelta(minutes=1))
    def create_tables():
        pg_hook = PostgresHook(postgres_conn_id='my_source_db')
        create_sql = """
        CREATE TABLE IF NOT EXISTS public.dim_property (
            region_name VARCHAR(20),
            property_id VARCHAR(20) PRIMARY KEY,
            construction_year INT,
            age INT
        );

        CREATE TABLE IF NOT EXISTS public.fact_prop_maintenance (
            property_id VARCHAR(20),
            repair_year INT,
            occupants INT,
            repair_count INT,
            total_repair_cost DECIMAL(10,2),
            FOREIGN KEY (property_id) REFERENCES public.dim_property(property_id)
        );
        """
        pg_hook.run(create_sql)
        return "Tables created successfully"

    @task(execution_timeout=timedelta(minutes=15), retries=2, retry_delay=timedelta(minutes=1))
    def extract() -> str:
        # Download CSV from MinIO
        conn = BaseHook.get_connection('minio_conn')
        s3 = boto3.client(
            's3',
            endpoint_url=conn.host,
            aws_access_key_id=conn.login,
            aws_secret_access_key=conn.password,
            region_name='us-east-1'
        )

        try:
            bucket = 'property-data'
            key = 'synthetic_property_data.csv'
            obj = s3.get_object(Bucket=bucket, Key=key)
            
            # Read CSV directly into pandas DataFrame
            df = pd.read_csv(io.BytesIO(obj['Body'].read()))
            
            # Save to parquet for faster processing
            parquet_path = '/tmp/prop_data.parquet'
            df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
            
            return parquet_path
            
        except Exception as e:
            print(f"Error in extract task: {e}")
            raise

    @task(execution_timeout=timedelta(minutes=15), retries=2, retry_delay=timedelta(minutes=1))
    def transform_and_load(parquet_path: str):
        # Load data from parquet
        df = pd.read_parquet(parquet_path)
        
        # Create dimension and fact dataframes
        dim_df = df[["region_name", "property_id", "construction_year"]].drop_duplicates()
        dim_df["age"] = pd.Timestamp.now().year - dim_df["construction_year"]
        fact_df = df[["property_id", "repair_year", "occupants", "repair_count", "total_repair_cost"]]
        
        # Get connection details from hook
        pg_hook = PostgresHook(postgres_conn_id='my_source_db')
        conn_uri = pg_hook.get_uri()
        
        # Create SQLAlchemy engine
        engine = create_engine(conn_uri)
        
        with engine.begin() as connection:
            # Clean target tables - use transaction to ensure atomicity
            connection.execute("DELETE FROM fact_prop_maintenance")
            connection.execute("DELETE FROM dim_property")
            
            # Load data to PostgreSQL
            dim_df.to_sql('dim_property', connection, if_exists='append', index=False, 
                         method='multi', chunksize=5000)
            fact_df.to_sql('fact_prop_maintenance', connection, if_exists='append', index=False, 
                          method='multi', chunksize=10000)
            
        # Clean up temp files
        try:
            if os.path.exists(parquet_path):
                os.remove(parquet_path)
        except Exception as e:
            print(f"Warning: Could not remove temporary file {parquet_path}: {e}")
            
        return f"Loaded {len(dim_df)} dimension records and {len(fact_df)} fact records"

    # Task chaining
    create_tables() >> transform_and_load(extract())

dag = load_property_maintenance_data()