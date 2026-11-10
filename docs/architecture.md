# Architecture and design notes

## Data flow

1. **Source simulation:** `generate_data.py` produces deterministic synthetic CRM opportunities and injects duplicate IDs, missing non-critical dimensions, inconsistent category casing, and invalid amounts.
2. **Ingestion:** the raw CSV is written to `data/raw/`.
3. **Transformation:** `transform.py` standardizes text, parses dates and numeric fields, deduplicates transaction IDs, rejects invalid records, fills non-critical categories, and derives revenue and month dimensions.
4. **Quality reporting:** the ETL records raw counts, duplicate IDs/rows removed, invalid rows excluded, cleaned rows, and remaining missing required values.
5. **Analytics mart:** the pipeline aggregates opportunities by month, region, lead source, sales rep, deal stage, and status.
6. **Warehouse:** the optional BigQuery loader uses explicit schemas, monthly date partitioning, and clustering on common filter dimensions.
7. **Visualization:** Looker Studio can read the aggregate mart.

## Data-quality rules

- `transaction_id`, `customer_id`, `created_date`, and `amount` are required.
- Transaction IDs are unique after deduplication; the last encountered row is retained.
- `amount` must be numeric and greater than zero.
- `probability` is coerced to numeric, defaults to zero when missing, and is constrained to 0–1.
- Text dimensions are trimmed and standardized to title case.
- Missing non-critical dimensions are labelled `Unknown`.
- Won revenue equals amount for Won records and zero for other statuses.

## BigQuery optimization choices

- The opportunity detail table is partitioned by `created_date` and clustered by `region`, `lead_source`, and `sales_rep`.
- The aggregate mart is partitioned by `month_start` and clustered by the same common filter dimensions.
- The dashboard reads the aggregate mart rather than repeatedly grouping the detail table.
- Production tuning should be verified with query plans and bytes-processed metrics in the target Google Cloud project; no unmeasured performance gain is claimed here.
