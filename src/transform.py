from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"

REQUIRED_COLUMNS = [
    "transaction_id", "customer_id", "lead_id", "sales_rep", "region",
    "lead_source", "product", "deal_stage", "created_date", "amount", "status"
]


def transform_sales_data(raw: pd.DataFrame):
    """Clean CRM records, create a sales mart, and return measured quality metrics."""
    df = raw.copy()
    raw_rows = len(df)

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    text_cols = [
        "transaction_id", "customer_id", "lead_id", "sales_rep",
        "region", "lead_source", "product", "deal_stage", "status", "email"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    for col in ["region", "lead_source", "product", "deal_stage", "status"]:
        df[col] = df[col].str.title()

    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    if "close_date" in df.columns:
        df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["probability"] = pd.to_numeric(df["probability"], errors="coerce")

    # Keep the last encountered record for each transaction ID.
    duplicate_mask = df.duplicated(subset=["transaction_id"], keep="last")
    duplicate_ids_detected = int(df.loc[duplicate_mask, "transaction_id"].nunique())
    duplicate_rows_removed = int(duplicate_mask.sum())
    df = df.loc[~duplicate_mask].copy()

    before_validation = len(df)
    valid_mask = (
        df["transaction_id"].notna()
        & df["customer_id"].notna()
        & df["created_date"].notna()
        & df["amount"].notna()
        & (df["amount"] > 0)
    )
    invalid_rows_excluded = int((~valid_mask).sum())
    df = df.loc[valid_mask].copy()

    # Non-critical dimensions are retained with an explicit fallback label.
    for col in ["sales_rep", "region", "lead_source", "product", "deal_stage"]:
        df[col] = df[col].fillna("Unknown")
    if "email" in df.columns:
        df["email"] = df["email"].fillna("")

    df["probability"] = df["probability"].fillna(0).clip(0, 1)
    df["revenue"] = df["amount"].where(df["status"].eq("Won"), 0.0)
    df["created_month"] = df["created_date"].dt.to_period("M").astype(str)
    df["month_start"] = df["created_date"].dt.to_period("M").dt.to_timestamp()
    df["created_year"] = df["created_date"].dt.year

    output_cols = [
        "transaction_id", "customer_id", "lead_id", "sales_rep", "region",
        "lead_source", "product", "deal_stage", "created_date", "close_date",
        "amount", "probability", "status", "email", "revenue",
        "created_month", "month_start", "created_year"
    ]
    df = df[[c for c in output_cols if c in df.columns]].sort_values(
        "created_date"
    ).reset_index(drop=True)

    mart = (
        df.groupby(
            ["created_month", "region", "lead_source", "sales_rep", "deal_stage", "status"],
            dropna=False
        )
        .agg(
            opportunity_count=("transaction_id", "nunique"),
            total_pipeline_value=("amount", "sum"),
            won_revenue=("revenue", "sum"),
            average_deal_size=("amount", "mean"),
            average_probability=("probability", "mean")
        )
        .reset_index()
    )
    mart["month_start"] = pd.to_datetime(mart["created_month"] + "-01")
    mart = mart[
        ["created_month", "month_start", "region", "lead_source", "sales_rep",
         "deal_stage", "status", "opportunity_count", "total_pipeline_value",
         "won_revenue", "average_deal_size", "average_probability"]
    ]
    mart["average_deal_size"] = mart["average_deal_size"].round(2)
    mart["average_probability"] = mart["average_probability"].round(4)
    mart["total_pipeline_value"] = mart["total_pipeline_value"].round(2)
    mart["won_revenue"] = mart["won_revenue"].round(2)

    report = {
        "raw_rows": int(raw_rows),
        "unique_duplicate_transaction_ids_detected": duplicate_ids_detected,
        "duplicate_rows_removed": duplicate_rows_removed,
        "rows_before_validation": int(before_validation),
        "invalid_rows_excluded": invalid_rows_excluded,
        "cleaned_rows": int(len(df)),
        "sales_mart_rows": int(len(mart)),
        "rows_removed_total": int(raw_rows - len(df)),
        "remaining_missing_required_values": {
            col: int(df[col].isna().sum()) for col in
            ["transaction_id", "customer_id", "created_date", "amount"]
        },
        "synthetic_data_notice": (
            "All records are synthetic; metrics describe this generated dataset only."
        ),
        "validation_rules": {
            "amount_must_be_positive": True,
            "transaction_id_deduplication": "keep_last_record",
            "non_critical_dimensions": "fill_with_Unknown"
        }
    }
    return df, mart, report


def save_outputs(cleaned: pd.DataFrame, mart: pd.DataFrame, report: dict):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_DIR / "cleaned_sales.csv", index=False)
    mart.to_csv(PROCESSED_DIR / "sales_mart.csv", index=False)
    with open(PROCESSED_DIR / "quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    pass
