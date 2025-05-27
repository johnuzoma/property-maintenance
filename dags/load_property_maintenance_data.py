from airflow.decorators import dag
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 4, 9),
    catchup=False,
    tags=["gcs", "bigquery", "raw_load"]
)
def load_raw_data_to_bigquery():

    gcs_uri = "gs://property-ju/synthetic_property_data.csv"

    load_job = BigQueryInsertJobOperator(
        task_id="load_raw_data_to_bigquery",
        configuration={
            "load": {
                "sourceUris": [gcs_uri],
                "destinationTable": {
                    "projectId": "practice-project-461104",
                    "datasetId": "property_data",
                    "tableId": "stg_property_maintenance"
                },
                "sourceFormat": "CSV",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        },
        gcp_conn_id="my_gcp_conn"
    )

    load_job

dag = load_raw_data_to_bigquery()
