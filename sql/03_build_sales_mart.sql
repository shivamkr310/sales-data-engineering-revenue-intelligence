-- Rebuild the reporting mart from the opportunity-level BigQuery table.
CREATE OR REPLACE TABLE `YOUR_PROJECT_ID.sales_analytics.sales_mart`
PARTITION BY DATE_TRUNC(month_start, MONTH)
CLUSTER BY region, lead_source, sales_rep AS
SELECT
  FORMAT_DATE('%Y-%m', DATE_TRUNC(created_date, MONTH)) AS created_month,
  DATE_TRUNC(created_date, MONTH) AS month_start,
  region,
  lead_source,
  sales_rep,
  deal_stage,
  status,
  COUNT(DISTINCT transaction_id) AS opportunity_count,
  SUM(amount) AS total_pipeline_value,
  SUM(revenue) AS won_revenue,
  AVG(amount) AS average_deal_size,
  AVG(probability) AS average_probability
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`
GROUP BY month_start, region, lead_source, sales_rep, deal_stage, status;
