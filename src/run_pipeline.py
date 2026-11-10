from pathlib import Path
from src.generate_data import generate_sales_data
from src.transform import transform_sales_data, save_outputs

ROOT = Path(__file__).resolve().parents[1]


def main():
    raw = generate_sales_data(n_rows=5000, seed=42)
    raw_path = ROOT / "data" / "raw" / "sales_raw.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(raw_path, index=False)

    cleaned, mart, report = transform_sales_data(raw)
    save_outputs(cleaned, mart, report)

    print("\nPIPELINE COMPLETED")
    print(f"Raw rows: {report['raw_rows']:,}")
    print(f"Duplicate rows removed: {report['duplicate_rows_removed']:,}")
    print(f"Invalid rows excluded: {report['invalid_rows_excluded']:,}")
    print(f"Clean rows: {report['cleaned_rows']:,}")
    print(f"Mart rows: {len(mart):,}")
    print("Outputs saved under data/processed/")


if __name__ == "__main__":
    main()
