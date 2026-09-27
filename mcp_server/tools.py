from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "E-commercecosmeticdataset.csv"


def load_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    return pd.read_csv(DATA_PATH, encoding="latin-1")


def list_dataset_columns() -> dict[str, list[str]]:
    df = load_dataset()
    return {"columns": list(df.columns)}


def get_dataset_summary() -> dict[str, Any]:
    df = load_dataset()
    return {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "nulls": df.isnull().sum().to_dict(),
        "sample": df.head(5).to_dict(orient="records"),
    }


def query_products(
    website: str | None = None,
    category: str | None = None,
    country: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> dict[str, Any]:
    df = load_dataset()

    if website:
        df = df[df["website"].fillna("").str.lower() == website.lower()]
    if category:
        df = df[df["category"].fillna("").str.lower() == category.lower()]
    if country:
        df = df[df["country"].fillna("").str.lower() == country.lower()]
    if brand:
        df = df[df["brand"].fillna("").str.lower() == brand.lower()]
    if min_price is not None:
        df = df[df["price"].astype(float) >= float(min_price)]
    if max_price is not None:
        df = df[df["price"].astype(float) <= float(max_price)]

    return {
        "count": int(len(df)),
        "rows": df.head(20).to_dict(orient="records"),
    }


def category_breakdown() -> dict[str, int]:
    df = load_dataset()
    return df.groupby("category").size().sort_values(ascending=False).to_dict()


def export_cleaned_dataset() -> dict[str, Any]:
    df = load_dataset()
    cleaned = df.drop(columns=["product_name", "title-href", "ingredients"], errors="ignore")
    output_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_products.csv"
    cleaned.to_csv(output_path, index=False)
    return {"path": str(output_path), "rows": int(len(cleaned))}
