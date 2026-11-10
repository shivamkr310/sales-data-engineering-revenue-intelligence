# Architecture and design notes

## Data flow

1. **Source simulation:** `generate_data.py` produces synthetic CRM opportunity records.
2. **Ingestion:** the raw CSV is written to `data/raw/`.
3. **Transformation:** `transform.py` standardizes text, parses dates, converts numeric fields, deduplicates transaction IDs, excludes invalid records, fills non-critical categories, and derives revenue/time dimensions.
4. **Data quality:** the ETL emits row counts, duplicate counts, excluded-row counts, and remaining missing required values.
5. **Analytics mart:** data is grouped by month, region, lead source, sales rep, deal stage, and status.
6. **Warehouse:** optional BigQuery uploader creates/replaces `cleaned_sales` and `sales_mart` tables.
7. **Visualization:** Looker Studio can read the sales mart.

## Data-quality rules

- `transaction_id`, `customer_id`, `created_date`, and `amount` are required.
- `transaction_id` must be unique after deduplication.
- `amount` must be numeric and non-negative.
- `probability` is constrained to the 0–1 range.
- Text dimensions are trimmed and normalized.
- Missing non-critical dimensions are labelled `Unknown`.
- Won revenue is `amount` only when status is `Won`; otherwise it is zero.

## Query optimization considerations

The sample mart aggregates data before dashboard consumption, reducing repeated high-cardinality calculations in the visualization layer. In BigQuery, production extensions should consider date partitioning, clustering by frequently filtered dimensions, selecting only required columns, and inspecting bytes processed and query execution details. This repository demonstrates the concepts; benchmark claims must be measured in the user's own BigQuery environment.
