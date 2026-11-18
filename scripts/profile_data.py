
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

primary_keys = {
    "customers": "customer_id",
    "employees": "employee_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "products": "product_id",
    "stores": "store_id",
}

tables = {}

for name, key in primary_keys.items():
    df = pd.read_csv(DATA_DIR / f"{name}.csv", dtype=str)
    tables[name] = df

    print(f"\n{'=' * 55}")
    print(f"TABLE: {name.upper()}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate primary keys: {df[key].duplicated().sum()}")
    print(f"Fully duplicate rows: {df.duplicated().sum()}")

    nulls = df.isna().sum()
    print("Null values:")
    print(nulls[nulls > 0].to_string() if nulls.any() else "None")

relationships = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("orders", "store_id", "stores", "store_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("employees", "store_id", "stores", "store_id"),
]

print("\nFOREIGN KEY VALIDATION")

for child, fk, parent, pk in relationships:
    missing = (
        tables[child][fk].notna()
        & ~tables[child][fk].isin(tables[parent][pk])
    )

    print(f"{child}.{fk} -> {parent}.{pk}: "
          f"{missing.sum()} orphan records")

print("\nFINANCIAL RECONCILIATION")

orders = tables["orders"].copy()
items = tables["order_items"].copy()

orders["total_amount"] = pd.to_numeric(
    orders["total_amount"], errors="coerce"
)
items["line_amount"] = pd.to_numeric(
    items["line_amount"], errors="coerce"
)

item_totals = (
    items.groupby("order_id")["line_amount"]
    .sum()
    .rename("calculated_total")
)

comparison = orders.join(
    item_totals, on="order_id"
)

difference = (
    comparison["total_amount"]
    - comparison["calculated_total"]
).abs()

mismatches = difference.gt(0.01) & difference.notna()

print(f"Orders with mismatched totals: {mismatches.sum()}")
print(f"Orders without matching items: "
      f"{comparison['calculated_total'].isna().sum()}")
