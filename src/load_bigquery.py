"""Load generated CRM CSV outputs into explicitly typed BigQuery tables.

Install requirements-cloud.txt and configure Application Default Credentials
before running this optional cloud integration.
"""
from __future__ import annotations

import os
from pathlib import Path

from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID", "sales_analytics")
LOCATION = os.getenv("BQ_LOCATION", "US")


def load_csv(client, csv_path: Path, table_id: str, schema) -> int:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"{csv_path} not found. Run python -m src.run_pipeline first."
        )
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=schema,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        max_bad_records=0,
    )
    with csv_path.open("rb") as source:
        job = client.load_table_from_file(
            source, table_id, job_config=config, location=LOCATION
        )
    job.result()
    loaded = int(client.get_table(table_id).num_rows)
    print(f"Loaded {loaded:,} rows into {table_id}")
    return loaded


def main() -> None:
    if not PROJECT_ID:
        raise EnvironmentError("Set GCP_PROJECT_ID before running the BigQuery loader.")

    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)
    dataset = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset.location = LOCATION
    client.create_dataset(dataset, exists_ok=True)

    cleaned_id = f"{PROJECT_ID}.{DATASET_ID}.cleaned_sales"
    cleaned_schema = [
        bigquery.SchemaField("transaction_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("lead_id", "STRING"),
        bigquery.SchemaField("sales_rep", "STRING"),
        bigquery.SchemaField("region", "STRING"),
        bigquery.SchemaField("lead_source", "STRING"),
        bigquery.SchemaField("product", "STRING"),
        bigquery.SchemaField("deal_stage", "STRING"),
        bigquery.SchemaField("created_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("close_date", "DATE"),
        bigquery.SchemaField("amount", "NUMERIC", mode="REQUIRED"),
        bigquery.SchemaField("probability", "FLOAT64"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("revenue", "NUMERIC"),
        bigquery.SchemaField("created_month", "STRING"),
        bigquery.SchemaField("month_start", "DATE"),
        bigquery.SchemaField("created_year", "INT64"),
    ]
    cleaned_table = bigquery.Table(cleaned_id, schema=cleaned_schema)
    cleaned_table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.MONTH, field="created_date"
    )
    cleaned_table.clustering_fields = ["region", "lead_source", "sales_rep"]
    client.create_table(cleaned_table, exists_ok=True)

    mart_id = f"{PROJECT_ID}.{DATASET_ID}.sales_mart"
    mart_schema = [
        bigquery.SchemaField("created_month", "STRING"),
        bigquery.SchemaField("month_start", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING"),
        bigquery.SchemaField("lead_source", "STRING"),
        bigquery.SchemaField("sales_rep", "STRING"),
        bigquery.SchemaField("deal_stage", "STRING"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("opportunity_count", "INT64"),
        bigquery.SchemaField("total_pipeline_value", "NUMERIC"),
        bigquery.SchemaField("won_revenue", "NUMERIC"),
        bigquery.SchemaField("average_deal_size", "NUMERIC"),
        bigquery.SchemaField("average_probability", "FLOAT64"),
    ]
    mart_table = bigquery.Table(mart_id, schema=mart_schema)
    mart_table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.MONTH, field="month_start"
    )
    mart_table.clustering_fields = ["region", "lead_source", "sales_rep"]
    client.create_table(mart_table, exists_ok=True)

    load_csv(client, ROOT / "data/processed/cleaned_sales.csv", cleaned_id, cleaned_schema)
    load_csv(client, ROOT / "data/processed/sales_mart.csv", mart_id, mart_schema)


if __name__ == "__main__":
    main()
