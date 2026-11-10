-- Run in BigQuery Studio after the Python ETL output is loaded.
SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT transaction_id) AS distinct_transaction_ids,
  COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_row_count,
  COUNTIF(transaction_id IS NULL OR transaction_id = '') AS missing_transaction_ids,
  COUNTIF(customer_id IS NULL OR customer_id = '') AS missing_customer_ids,
  COUNTIF(created_date IS NULL) AS missing_created_dates
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`;

-- Invalid monetary values and probabilities (expected result: no rows).
SELECT *
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`
WHERE amount <= 0 OR probability < 0 OR probability > 1;

-- Revenue reconciliation (expected difference: zero).
SELECT
  SUM(revenue) AS loaded_revenue,
  SUM(IF(status = 'Won', amount, 0)) AS expected_won_revenue,
  SUM(revenue) - SUM(IF(status = 'Won', amount, 0)) AS reconciliation_difference
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`;

-- Mart grain uniqueness (expected result: no rows).
SELECT created_month, region, lead_source, sales_rep, deal_stage, status,
       COUNT(*) AS rows_at_grain
FROM `YOUR_PROJECT_ID.sales_analytics.sales_mart`
GROUP BY created_month, region, lead_source, sales_rep, deal_stage, status
HAVING COUNT(*) > 1;
