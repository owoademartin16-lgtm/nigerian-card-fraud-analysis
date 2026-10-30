"""Build the compact dashboard aggregates from the already-cleaned fraud dataset.

The notebook loads the public Hugging Face dataset and only downcasts dtypes and
adds time columns. This script reads the local Arrow cache of that same cleaned
data (or a directory passed with --arrow-dir) and writes small aggregates for the
Streamlit app. It does not re-clean, impute, or filter the source rows.
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa

DEFAULT_CACHE = (
    "/Users/user/.cache/huggingface/datasets/"
    "electricsheepafrica___nigerian-banking-retail-transactions/"
    "default/0.0.0/c31e7981f3a935fc9142923fd082143a4204b4f9"
)

AMOUNT_BINS = [-np.inf, 1000, 5000, 10000, 50000, 100000, np.inf]
AMOUNT_LABELS = [
    "₦0–₦1,000", "₦1,001–₦5,000", "₦5,001–₦10,000",
    "₦10,001–₦50,000", "₦50,001–₦100,000", "Above ₦100,000",
]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def read_arrow_dir(path: Path) -> pd.DataFrame:
    files = sorted(glob.glob(str(path / "*.arrow")))
    if not files:
        raise FileNotFoundError(f"No .arrow files in {path}")
    tables = []
    for f in files:
        with pa.memory_map(f, "r") as source:
            tables.append(pa.ipc.open_stream(source).read_all())
    table = pa.concat_tables(tables)
    cols = [
        "timestamp", "amount_ngn", "transaction_type", "channel",
        "merchant_category_code", "location_state", "fraud_flag",
    ]
    return table.select(cols).to_pandas()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arrow-dir", default=DEFAULT_CACHE)
    ap.add_argument("--out", default="data")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print("reading", args.arrow_dir)
    df = read_arrow_dir(Path(args.arrow_dir))
    print("rows", f"{len(df):,}")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["month"] = df["timestamp"].dt.strftime("%Y-%m")
    df["hour"] = df["timestamp"].dt.hour.astype("int8")
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["amount_group"] = pd.cut(
        df["amount_ngn"], bins=AMOUNT_BINS, labels=AMOUNT_LABELS
    )
    df["fraud_amount"] = np.where(df["fraud_flag"], df["amount_ngn"], 0.0)

    # Headline figures, exactly as the notebook reports them.
    total_transactions = int(len(df))
    total_fraud = int(df["fraud_flag"].sum())
    total_value = float(df["amount_ngn"].sum())
    fraud_value = float(df["fraud_amount"].sum())
    legit = df[~df["fraud_flag"]]
    fraud = df[df["fraud_flag"]]
    headline = {
        "total_transactions": total_transactions,
        "fraud_transactions": total_fraud,
        "fraud_rate_pct": total_fraud / total_transactions * 100,
        "total_value_ngn": total_value,
        "fraud_value_ngn": fraud_value,
        "fraud_value_share_pct": fraud_value / total_value * 100,
        "avg_transaction_ngn": float(df["amount_ngn"].mean()),
        "avg_fraud_ngn": float(fraud["amount_ngn"].mean()),
        "avg_legit_ngn": float(legit["amount_ngn"].mean()),
        "overnight_fraud": int(fraud["hour"].isin([22, 23, 0, 1, 2, 3, 4, 5, 6]).sum()),
        "overnight_fraud_share_pct": float(
            fraud["hour"].isin([22, 23, 0, 1, 2, 3, 4, 5, 6]).mean() * 100
        ),
        "overnight_transactions": int(
            df["hour"].isin([22, 23, 0, 1, 2, 3, 4, 5, 6]).sum()
        ),
    }
    (out / "headline.json").write_text(json.dumps(headline, indent=2), encoding="utf-8")
    print(json.dumps(headline, indent=2)[:1200])

    # Main cube: supports every sidebar filter and every filtered chart except
    # day-of-week and merchant category, which are kept as all-period context.
    keys = ["month", "hour", "channel", "location_state", "transaction_type", "amount_group"]
    for col in ["month", "channel", "location_state", "transaction_type", "amount_group"]:
        df[col] = df[col].astype("category")

    cube = (
        df.groupby(keys, observed=True, dropna=False)
        .agg(
            total_transactions=("fraud_flag", "size"),
            fraud_transactions=("fraud_flag", "sum"),
            total_amount=("amount_ngn", "sum"),
            fraud_amount=("fraud_amount", "sum"),
        )
        .reset_index()
    )
    cube["total_transactions"] = cube["total_transactions"].astype("int32")
    cube["fraud_transactions"] = cube["fraud_transactions"].astype("int32")
    cube["total_amount"] = cube["total_amount"].astype("float64")
    cube["fraud_amount"] = cube["fraud_amount"].astype("float64")
    cube.to_parquet(out / "fraud_cube.parquet", index=False, compression="zstd")
    print("cube", cube.shape, (out / "fraud_cube.parquet").stat().st_size / 1e6, "MB")

    day = (
        df.groupby("day_of_week", observed=True)
        .agg(
            total_transactions=("fraud_flag", "size"),
            fraud_transactions=("fraud_flag", "sum"),
            fraud_amount=("fraud_amount", "sum"),
        )
        .reindex(DAY_ORDER)
        .reset_index()
    )
    day["fraud_rate_pct"] = day["fraud_transactions"] / day["total_transactions"] * 100
    day.to_csv(out / "day_summary.csv", index=False)
    print(day.to_string(index=False))

    cat = (
        df.groupby("merchant_category_code", observed=True)
        .agg(
            total_transactions=("fraud_flag", "size"),
            fraud_transactions=("fraud_flag", "sum"),
            fraud_amount=("fraud_amount", "sum"),
        )
        .reset_index()
    )
    cat["fraud_rate_pct"] = cat["fraud_transactions"] / cat["total_transactions"] * 100
    cat = cat.sort_values(["fraud_rate_pct", "total_transactions"], ascending=[False, False])
    cat.to_csv(out / "category_summary.csv", index=False)
    print(cat.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
