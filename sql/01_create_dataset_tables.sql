-- Run in BigQuery Studio after replacing YOUR_PROJECT_ID.
CREATE SCHEMA IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics`;

-- Reference table definitions. The Python BigQuery uploader uses autodetect;
-- these DDL statements document the intended logical schema.
CREATE TABLE IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics.cleaned_sales` (
  transaction_id STRING,
  customer_id STRING,
  lead_id STRING,
  sales_rep STRING,
  region STRING,
  lead_source STRING,
  product STRING,
  deal_stage STRING,
  created_date TIMESTAMP,
  close_date TIMESTAMP,
  amount FLOAT64,
  probability FLOAT64,
  status STRING,
  email STRING,
  revenue FLOAT64,
  created_month STRING,
  created_year INT64
);

CREATE TABLE IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics.sales_mart` (
  created_month STRING,
  region STRING,
  lead_source STRING,
  sales_rep STRING,
  deal_stage STRING,
  status STRING,
  opportunity_count INT64,
  total_pipeline_value FLOAT64,
  won_revenue FLOAT64,
  average_deal_size FLOAT64,
  average_probability FLOAT64
);
