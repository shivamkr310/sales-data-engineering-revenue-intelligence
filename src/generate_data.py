from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def generate_sales_data(n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Create deterministic synthetic CRM data with intentional quality issues."""
    rng = np.random.default_rng(seed)

    regions = np.array(["North", "South", "East", "West"])
    reps = np.array(["Aarav Shah", "Maya Iyer", "Rohan Das", "Sara Khan", "Dev Patel"])
    sources = np.array(["Website", "Referral", "LinkedIn", "Webinar", "Email"])
    products = np.array(["Analytics", "Automation", "CRM", "Consulting"])
    stages = np.array(["New", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"])

    created = pd.Timestamp("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 630, size=n_rows), unit="D"
    )
    status = rng.choice(
        ["Open", "Won", "Lost"], size=n_rows, p=[0.42, 0.36, 0.22]
    )
    stage_map = {
        "Open": ["New", "Qualified", "Proposal", "Negotiation"],
        "Won": ["Closed Won"],
        "Lost": ["Closed Lost"],
    }
    deal_stage = [rng.choice(stage_map[s]) for s in status]

    amount = np.round(rng.lognormal(mean=8.2, sigma=0.75, size=n_rows), 2)
    close_dates = []
    for i, s in enumerate(status):
        if s == "Open":
            close_dates.append(pd.NaT)
        else:
            close_dates.append(
                created[i] + pd.to_timedelta(int(rng.integers(5, 100)), unit="D")
            )

    df = pd.DataFrame({
        "transaction_id": [f"TXN-{i+1:06d}" for i in range(n_rows)],
        "customer_id": [f"CUST-{x:05d}" for x in rng.integers(1, 1800, size=n_rows)],
        "lead_id": [f"LEAD-{i+1:06d}" for i in range(n_rows)],
        "sales_rep": rng.choice(reps, size=n_rows),
        "region": rng.choice(regions, size=n_rows),
        "lead_source": rng.choice(sources, size=n_rows),
        "product": rng.choice(products, size=n_rows),
        "deal_stage": deal_stage,
        "created_date": created,
        "close_date": close_dates,
        "amount": amount,
        "probability": np.round(rng.uniform(0.05, 0.95, size=n_rows), 2),
        "status": status,
        "email": [
            f"customer{x:05d}@example.test" for x in rng.integers(1, 1800, size=n_rows)
        ],
    })

    # Controlled issues for the ETL process to identify and handle.
    duplicate_idx = rng.choice(
        df.index, size=max(1, int(n_rows * 0.02)), replace=False
    )
    duplicate_rows = df.loc[duplicate_idx].copy()
    # Keep the same transaction IDs but slightly alter non-key values.
    duplicate_rows["amount"] = duplicate_rows["amount"] * 1.03
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    missing_region_idx = rng.choice(df.index, size=int(len(df) * 0.01), replace=False)
    df.loc[missing_region_idx, "region"] = None

    missing_email_idx = rng.choice(df.index, size=int(len(df) * 0.025), replace=False)
    df.loc[missing_email_idx, "email"] = None

    inconsistent_idx = rng.choice(df.index, size=int(len(df) * 0.02), replace=False)
    df.loc[inconsistent_idx, "region"] = (
        df.loc[inconsistent_idx, "region"].astype("string").str.lower()
    )

    invalid_amount_idx = rng.choice(
        df.index, size=max(1, int(len(df) * 0.003)), replace=False
    )
    df.loc[invalid_amount_idx, "amount"] = -1

    return df


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_sales_data()
    out = RAW_DIR / "sales_raw.csv"
    df.to_csv(out, index=False)
    print(f"Generated {len(df):,} raw rows: {out}")


if __name__ == "__main__":
    main()
