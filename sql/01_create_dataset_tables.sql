-- BigQuery Standard SQL. Replace YOUR_PROJECT_ID before execution.
CREATE SCHEMA IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics`
OPTIONS(location = "US");

CREATE TABLE IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics.cleaned_sales` (
  transaction_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  lead_id STRING,
  sales_rep STRING,
  region STRING,
  lead_source STRING,
  product STRING,
  deal_stage STRING,
  created_date DATE NOT NULL,
  close_date DATE,
  amount NUMERIC NOT NULL,
  probability FLOAT64,
  status STRING,
  email STRING,
  revenue NUMERIC,
  created_month STRING,
  month_start DATE,
  created_year INT64
)
PARTITION BY DATE_TRUNC(created_date, MONTH)
CLUSTER BY region, lead_source, sales_rep;

CREATE TABLE IF NOT EXISTS `YOUR_PROJECT_ID.sales_analytics.sales_mart` (
  created_month STRING,
  month_start DATE NOT NULL,
  region STRING,
  lead_source STRING,
  sales_rep STRING,
  deal_stage STRING,
  status STRING,
  opportunity_count INT64,
  total_pipeline_value NUMERIC,
  won_revenue NUMERIC,
  average_deal_size NUMERIC,
  average_probability FLOAT64
)
PARTITION BY DATE_TRUNC(month_start, MONTH)
CLUSTER BY region, lead_source, sales_rep;
