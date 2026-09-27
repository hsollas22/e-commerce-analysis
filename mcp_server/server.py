from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

from mcp_server.tools import (
    category_breakdown,
    export_cleaned_dataset,
    get_dataset_summary,
    list_dataset_columns,
    query_products,
)

mcp = FastMCP("ecomm-data")


@mcp.tool(description="Return the column names from the e-commerce product dataset.")
def dataset_columns() -> dict[str, list[str]]:
    """Return the column names from the e-commerce product dataset."""
    return list_dataset_columns()


@mcp.tool(description="Return a summary of the dataset with shape, nulls, and a preview of the rows.")
def dataset_summary() -> dict:
    """Return a summary of the dataset with shape, nulls, and a preview of the rows."""
    return get_dataset_summary()


@mcp.tool(
    description="Filter the e-commerce dataset by website, category, country, brand, and optional price range."
)
def products(
    website: str | None = None,
    category: str | None = None,
    country: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> dict:
    """Filter the product catalog by optional website, category, country, brand, and price range."""
    return query_products(
        website=website,
        category=category,
        country=country,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
    )


@mcp.tool(description="Return the number of products in each category for the e-commerce dataset.")
def category_summary() -> dict:
    """Return the number of products in each category."""
    return category_breakdown()


@mcp.tool(description="Export a cleaned version of the product catalog to a CSV file in the data folder.")
def cleaned_products_export() -> dict:
    """Export a cleaned version of the product catalog to a CSV file in the data folder."""
    return export_cleaned_dataset()


if __name__ == "__main__":
    mcp.run()
