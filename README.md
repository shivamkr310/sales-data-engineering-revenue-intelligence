# Sales Data Engineering & Revenue Intelligence Platform

A portfolio project for turning messy CRM-style sales opportunities into clean, analysis-ready datasets and reporting tables with Python, Pandas, and SQL.

> **Data note:** Every record is synthetic and generated locally for this project. It is not real company, customer, or employer data. The core ETL runs locally; BigQuery and Looker Studio are optional extensions.

## What the pipeline does

- Generates 5,000 synthetic CRM opportunity records and adds controlled data-quality issues and duplicate rows.
- Normalizes text and dates, deduplicates transaction IDs, validates key fields, and handles missing non-critical dimensions.
- Derives recognized revenue and time dimensions.
- Produces a cleaned detail dataset, an aggregated sales mart, and a JSON quality report.
- Includes BigQuery Standard SQL for schema setup, data-quality checks, and reporting.
- Includes an optional BigQuery uploader, a Looker Studio dashboard guide, automated tests, and GitHub Actions CI.

## Verified local run

Latest run with the deterministic generator seed (`42`):

| Measure | Result |
|---|---:|
| Raw rows generated | 5,100 |
| Duplicate rows removed | 100 |
| Invalid rows excluded | 15 |
| Clean detail rows | 4,985 |
| Aggregated sales-mart rows | 3,932 |
| Automated tests | 2 passed |

These values describe the generated synthetic dataset only. They are not commercial outcomes or performance improvements for a real business.

## Architecture

```text
Synthetic CRM data generator
            |
            v
         Raw CSV
            |
            v
     Python / Pandas ETL
     - normalize fields
     - parse dates and numbers
     - deduplicate transaction IDs
     - validate records
            |
       +----+----------------+
       |                     |
       v                     v
 Clean detail data     JSON quality report
       |
       v
 Aggregated sales mart
       |
       +-----------------------+
       |                       |
       v                       v
 BigQuery SQL / tables   Looker Studio report
       (optional)             (optional)
```

## Repository structure

```text
.
├── .github/workflows/tests.yml
├── data/processed/quality_report.json
├── docs/
│   ├── architecture.md
│   └── dashboard_guide.md
├── sql/
│   ├── 01_create_dataset_tables.sql
│   ├── 02_data_quality_checks.sql
│   └── 03_build_sales_mart.sql
├── src/
│   ├── generate_data.py
│   ├── transform.py
│   ├── run_pipeline.py
│   └── load_bigquery.py
├── tests/test_transform.py
├── requirements.txt
└── .gitignore
```

The raw and processed CSV files are generated locally when the pipeline runs and are excluded from Git to keep the repository source-focused. The checked-in quality report records the results from the verified sample run.

## Run locally

### Requirements

- Python 3.10+
- pip

### Setup

```bash
git clone https://github.com/shivamkr310/sales-data-engineering-revenue-intelligence.git
cd sales-data-engineering-revenue-intelligence
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the ETL pipeline

```bash
python -m src.run_pipeline
```

The command creates `data/raw/sales_raw.csv` and refreshes these outputs:

- `data/processed/cleaned_sales.csv`
- `data/processed/sales_mart.csv`
- `data/processed/quality_report.json`

The generator uses a fixed seed, so the sample data and quality counts are reproducible.

### Run tests

```bash
python -m pytest -q
```

## SQL analytics

The `sql/` directory contains BigQuery Standard SQL:

1. `01_create_dataset_tables.sql` — reference schemas for the cleaned detail table and sales mart.
2. `02_data_quality_checks.sql` — duplicate, required-field, monetary-value, probability, and revenue-reconciliation checks.
3. `03_build_sales_mart.sql` — grouped reporting table.

Replace `YOUR_PROJECT_ID` with your Google Cloud project ID before running the scripts in BigQuery Studio.

## Optional BigQuery load

Google Cloud is not required for the local pipeline. To use the optional uploader:

1. Create a Google Cloud project and a dataset named `sales_analytics`.
2. Enable the BigQuery API.
3. Install the optional dependency: `pip install google-cloud-bigquery`.
4. Authenticate using Application Default Credentials: `gcloud auth application-default login`.
5. Set `GCP_PROJECT_ID` and run the uploader.

**PowerShell**
```powershell
$env:GCP_PROJECT_ID="your-gcp-project-id"
python -m src.load_bigquery
```

**macOS / Linux**
```bash
export GCP_PROJECT_ID="your-gcp-project-id"
python -m src.load_bigquery
```

The cloud load is an optional extension and is not represented as completed unless you configure and execute it in your own Google Cloud account.

## Looker Studio

See [docs/dashboard_guide.md](docs/dashboard_guide.md) for the recommended scorecards, trends, breakdowns, filters, and validation steps. The dashboard can use the BigQuery sales mart after loading, or the locally generated `sales_mart.csv` as a file source.

This repository contains dashboard instructions, not a published Looker Studio report.

## Quality and scope

The ETL report tracks raw rows, duplicate IDs and rows removed, invalid records excluded, cleaned row count, and remaining missing values in key fields. See [data/processed/quality_report.json](data/processed/quality_report.json) for the verified sample run.

This is a portfolio-scale demonstration, not a production revenue system. Possible extensions include incremental loads, explicit warehouse schemas, partitioning and clustering, orchestration, dbt models, and query-cost benchmarking.
