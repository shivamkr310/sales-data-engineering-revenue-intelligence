"""Optional uploader for generated CSV outputs to Google BigQuery."""
import os
from pathlib import Path
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID", "sales_analytics")


def upload_csv(client, path: Path, table_id: str):
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run python -m src.run_pipeline first."
        )

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with path.open("rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    print(f"Loaded {client.get_table(table_ref).num_rows:,} rows into {table_ref}")


def main():
    if not PROJECT_ID:
        raise EnvironmentError("Set GCP_PROJECT_ID before running this optional uploader.")

    client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    client.create_dataset(dataset_ref, exists_ok=True)

    upload_csv(client, ROOT / "data/processed/cleaned_sales.csv", "cleaned_sales")
    upload_csv(client, ROOT / "data/processed/sales_mart.csv", "sales_mart")


if __name__ == "__main__":
    main()
