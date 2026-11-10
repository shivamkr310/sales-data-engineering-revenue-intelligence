# Sales Data Engineering & Revenue Intelligence Platform

A portfolio project that converts messy CRM-style sales data into validated, analysis-ready datasets and reporting tables using Python, Pandas, and SQL.

> **Data notice:** The dataset is synthetic and generated specifically for this project. It does not represent a real company, customer, or employer. BigQuery and Looker Studio are optional extensions; the local pipeline works without cloud credentials.

## What it does

- Generates 5,000 synthetic CRM opportunity records, with controlled quality issues and duplicate records.
- Normalizes text and date fields, deduplicates transaction IDs, and validates key fields and amounts.
- Produces a cleaned detail dataset, an aggregated sales mart, and a JSON data-quality report.
- Includes BigQuery Standard SQL for table setup, validation, and reporting.
- Provides an optional BigQuery loader and a Looker Studio dashboard guide.

## Verified local run

| Measure | Result |
|---|---:|
| Raw rows generated | 5,100 |
| Duplicate rows removed | 100 |
| Invalid rows excluded | 15 |
| Clean detail rows | 4,985 |
| Aggregated sales-mart rows | 3,932 |
| Automated tests | 2 passed |

These counts describe the generated synthetic dataset only. They are not business results or client outcomes.

## Architecture

```text
Synthetic CRM generator
        |
        v
     Raw CSV
        |
        v
Python / Pandas ETL
  - normalize fields
  - parse and validate dates
  - deduplicate transaction IDs
  - validate required fields and amounts
        |
        +--------------------+
        |                    |
        v                    v
Clean detail CSV      Quality report (JSON)
        |
        v
Aggregated sales mart
        |
        +----------------------+
        |                      |
        v                      v
SQL analytics           Optional BigQuery
                               |
                               v
                         Looker Studio
```

## Repository structure

```text
.
├── data/
│   ├── raw/sales_raw.csv
│   └── processed/
│       ├── cleaned_sales.csv
│       ├── sales_mart.csv
│       └── quality_report.json
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
├── tests/
│   └── test_transform.py
├── requirements.txt
└── .gitignore
```

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

Activate the environment:

**Windows PowerShell**
```powershell
.venv\\Scripts\\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

### Run the ETL pipeline

```bash
python -m src.run_pipeline
```

The command regenerates the raw source and refreshes the cleaned dataset, sales mart, and quality report under `data/`.

### Run tests

```bash
python -m pytest -q
```

## SQL analytics

The `sql/` directory contains BigQuery Standard SQL:

1. `01_create_dataset_tables.sql` — reference table definitions.
2. `02_data_quality_checks.sql` — checks for missing values, duplicates, and invalid amounts.
3. `03_build_sales_mart.sql` — reporting aggregation.

Replace `YOUR_PROJECT_ID` before running the scripts in BigQuery.

## Optional BigQuery load

The local pipeline does not require Google Cloud. To use the optional loader:

1. Create a Google Cloud project and a dataset named `sales_analytics`.
2. Enable the BigQuery API and install `google-cloud-bigquery`.
3. Authenticate with Application Default Credentials: `gcloud auth application-default login`.
4. Set `GCP_PROJECT_ID` and run the loader.

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

Cloud loading is optional and has not been claimed as completed unless you configure and execute it in your own Google Cloud account.

## Looker Studio

See [docs/dashboard_guide.md](docs/dashboard_guide.md) for suggested KPI cards, trends, breakdowns, and filters. Use the BigQuery sales mart after loading, or upload `data/processed/sales_mart.csv` as a file-based source.

This repository contains the data and dashboard guide, not a published Looker Studio report.

## Data quality approach

The pipeline reports raw row count, duplicate transaction IDs, duplicate rows removed, invalid records excluded, cleaned row count, and remaining nulls in key fields. The measured result is stored in `data/processed/quality_report.json`.

## Scope and possible extensions

This is a portfolio-scale data workflow, not a production revenue system. Possible extensions include incremental loads, explicit warehouse schemas, partitioning and clustering, orchestration, dbt models, and CI automation.
