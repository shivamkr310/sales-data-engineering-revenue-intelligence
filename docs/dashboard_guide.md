# Looker Studio dashboard guide

## Connect a data source

### BigQuery option
1. Open Looker Studio and create a blank report.
2. Add data → BigQuery.
3. Select your Google Cloud project.
4. Select dataset `sales_analytics` and table `sales_mart`.
5. Add the data source to the report.

### CSV option
1. Run the local pipeline.
2. In Looker Studio, add data → File Upload (if available in your account).
3. Upload `data/processed/sales_mart.csv`.
4. Confirm the field types before building charts.

## Recommended dashboard layout

### Header KPI scorecards
Create calculated fields or scorecards for:
- **Won Revenue:** `SUM(won_revenue)`
- **Pipeline Value:** `SUM(total_pipeline_value)`
- **Opportunities:** `SUM(opportunity_count)`
- **Average Deal Size:** `AVG(average_deal_size)`

For win rate, use a detail-level source or create a separate summary query: `won opportunities / all closed opportunities`. Do not calculate win rate by averaging grouped percentages.

### Charts
1. Time series: `created_month` vs `SUM(won_revenue)`.
2. Bar chart: `sales_rep` vs `SUM(won_revenue)`.
3. Bar chart: `region` vs `SUM(total_pipeline_value)`.
4. Bar chart: `lead_source` vs `SUM(opportunity_count)`.
5. Table: `deal_stage`, `status`, `opportunity_count`, `total_pipeline_value`, `won_revenue`.

### Filters
Add controls for:
- created month
- region
- lead source
- sales representative
- deal stage

## Dashboard validation

Compare dashboard totals with the SQL reconciliation query in `sql/02_data_quality_checks.sql`. Validate date ranges and aggregation grain before presenting the dashboard as accurate.
