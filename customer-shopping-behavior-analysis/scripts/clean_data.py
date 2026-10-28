"""Clean and transform the raw customer shopping dataset.

Usage:
    python scripts/clean_data.py
Output:
    data/processed/customer_shopping_behavior_clean.csv
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "customer_shopping_behavior.csv"
OUT = ROOT / "data" / "processed" / "customer_shopping_behavior_clean.csv"

FREQUENCY_MAPPING = {
    "Weekly": 7,
    "Fortnightly": 14,
    "Bi-Weekly": 14,
    "Monthly": 30,
    "Quarterly": 90,
    "Every 3 Months": 90,
    "Annually": 365,
}
AGE_LABELS = ["Young Adult", "Adult", "Middle-aged", "Senior"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Impute missing review ratings with the median rating of the product category
    df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
        lambda s: s.fillna(s.median())
    )

    # 2. Snake-case column names
    df.columns = (
        df.columns.str.lower()
        .str.replace(" (usd)", "", regex=False)
        .str.replace(" ", "_")
    )

    # 3. Feature engineering
    df["age_group"] = pd.qcut(df["age"], q=4, labels=AGE_LABELS)
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(FREQUENCY_MAPPING)

    # 4. Drop redundant column (identical to discount_applied)
    if (df["discount_applied"] == df["promo_code_used"]).all():
        df = df.drop(columns="promo_code_used")

    return df


def main() -> None:
    df = pd.read_csv(RAW, encoding="utf-8-sig")
    print(f"Raw shape: {df.shape} | missing review ratings: {df['Review Rating'].isna().sum()}")
    cleaned = clean(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUT, index=False)
    print(f"Clean shape: {cleaned.shape} | nulls left: {int(cleaned.isna().sum().sum())}")
    print(f"Saved -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
