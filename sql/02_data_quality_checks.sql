-- 1. Duplicate transaction IDs (expected result: zero after the Python ETL).
SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT transaction_id) AS distinct_transaction_ids,
  COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_row_count
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`;

-- 2. Required-field completeness.
SELECT
  COUNTIF(transaction_id IS NULL OR transaction_id = '') AS missing_transaction_id,
  COUNTIF(customer_id IS NULL OR customer_id = '') AS missing_customer_id,
  COUNTIF(created_date IS NULL) AS missing_created_date,
  COUNTIF(amount IS NULL) AS missing_amount
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`;

-- 3. Invalid monetary values and probabilities.
SELECT *
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`
WHERE amount < 0
   OR probability < 0
   OR probability > 1;

-- 4. Revenue reconciliation: revenue should equal won amount only.
SELECT
  SUM(revenue) AS total_revenue,
  SUM(IF(status = 'Won', amount, 0)) AS expected_won_revenue,
  SUM(revenue) - SUM(IF(status = 'Won', amount, 0)) AS reconciliation_difference
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`;
