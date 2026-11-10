import pandas as pd
from src.transform import transform_sales_data


def sample_data():
    return pd.DataFrame([
        {
            "transaction_id": "T1", "customer_id": "C1", "lead_id": "L1",
            "sales_rep": " rep one ", "region": "north", "lead_source": "website",
            "product": "analytics", "deal_stage": "closed won",
            "created_date": "2025-01-05", "close_date": "2025-01-10",
            "amount": "1000", "probability": "0.8", "status": "won",
            "email": None
        },
        {
            "transaction_id": "T1", "customer_id": "C1", "lead_id": "L1",
            "sales_rep": "rep one", "region": "north", "lead_source": "website",
            "product": "analytics", "deal_stage": "closed won",
            "created_date": "2025-01-05", "close_date": "2025-01-10",
            "amount": "1050", "probability": "0.8", "status": "won",
            "email": "a@example.test"
        },
        {
            "transaction_id": "T2", "customer_id": "C2", "lead_id": "L2",
            "sales_rep": "rep two", "region": None, "lead_source": "referral",
            "product": "crm", "deal_stage": "proposal",
            "created_date": "2025-01-07", "close_date": None,
            "amount": "-5", "probability": "0.4", "status": "open",
            "email": "b@example.test"
        }
    ])


def test_deduplication_and_validation():
    cleaned, mart, report = transform_sales_data(sample_data())
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["transaction_id"] == "T1"
    assert report["duplicate_rows_removed"] == 1
    assert report["invalid_rows_excluded"] == 1


def test_won_revenue():
    cleaned, _, _ = transform_sales_data(sample_data())
    assert float(cleaned.iloc[0]["revenue"]) == 1050.0
    assert cleaned.iloc[0]["region"] == "North"
