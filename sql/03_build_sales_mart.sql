CREATE OR REPLACE TABLE `YOUR_PROJECT_ID.sales_analytics.sales_mart` AS
SELECT
  created_month,
  region,
  lead_source,
  sales_rep,
  deal_stage,
  status,
  COUNT(DISTINCT transaction_id) AS opportunity_count,
  ROUND(SUM(amount), 2) AS total_pipeline_value,
  ROUND(SUM(revenue), 2) AS won_revenue,
  ROUND(AVG(amount), 2) AS average_deal_size,
  ROUND(AVG(probability), 4) AS average_probability
FROM `YOUR_PROJECT_ID.sales_analytics.cleaned_sales`
GROUP BY
  created_month, region, lead_source, sales_rep, deal_stage, status;
