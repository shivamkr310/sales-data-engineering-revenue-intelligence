# Looker Studio revenue dashboard guide

This guide builds a Looker Studio report on the BigQuery table `sales_analytics.sales_mart`. The repository contains the data model and build instructions; a live report must be created and shared from the account that owns the Google Cloud project.

## Connect BigQuery

1. Open Looker Studio and create a blank report.
2. Choose **Add data → BigQuery**.
3. Select the Google Cloud project and `sales_analytics` dataset.
4. Select `sales_mart` and add it to the report.
5. Confirm `month_start` is a Date field and amount/revenue fields are numeric.

## Scorecards

| KPI | Metric | Aggregation |
|---|---|---|
| Won revenue | `won_revenue` | SUM |
| Opportunity value | `total_pipeline_value` | SUM |
| Opportunities | `opportunity_count` | SUM |
| Won opportunities | `opportunity_count` filtered to status = Won | SUM |

Create a calculated field for **Closed-deal win rate**:

```text
SUM(CASE WHEN status = "Won" THEN opportunity_count ELSE 0 END)
/
SUM(CASE WHEN status IN ("Won", "Lost") THEN opportunity_count ELSE 0 END)
```

Create a weighted **Average deal size** field rather than averaging the pre-aggregated average:

```text
SUM(total_pipeline_value) / SUM(opportunity_count)
```

Format win rate as a percentage and financial fields as USD currency.

## Charts

1. **Monthly revenue trend:** Time series; date = `month_start`; metric = SUM(`won_revenue`).
2. **Revenue by sales representative:** Bar chart; dimension = `sales_rep`; metric = SUM(`won_revenue`).
3. **Opportunity value by region:** Bar chart; dimension = `region`; metric = SUM(`total_pipeline_value`).
4. **Opportunity mix by lead source:** Bar chart; dimension = `lead_source`; metric = SUM(`opportunity_count`).
5. **Stage/status detail:** Table with `deal_stage`, `status`, SUM(`opportunity_count`), SUM(`total_pipeline_value`), and SUM(`won_revenue`).

## Filters

Add controls for `month_start`, `region`, `lead_source`, `sales_rep`, `deal_stage`, and `status`.

## Validate before sharing

- Compare totals with the BigQuery quality and reconciliation SQL.
- Use Won + Lost opportunities as the closed-deal win-rate denominator; exclude Open opportunities.
- Do not use AVG(`average_deal_size`) on the grouped mart; use the weighted formula above.
- Keep the synthetic-data notice visible in the report description.

## Optional CSV-only demo

Run `python -m src.run_pipeline` and connect `data/processed/sales_mart.csv` using the file-upload connector available in your Looker Studio account. Confirm numeric and date field types manually.
