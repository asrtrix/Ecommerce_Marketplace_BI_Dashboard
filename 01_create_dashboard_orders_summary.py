# %%
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path.cwd()

RAW_DIR = BASE_DIR / "raw_data"
CLEAN_DIR = BASE_DIR / "cleaned_data"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

print("Current working folder:", BASE_DIR)
print("Raw data folder:", RAW_DIR)
print("Cleaned data folder:", CLEAN_DIR)

# %% Cell 2: Load all raw CSV files

customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
geolocation = pd.read_csv(RAW_DIR / "olist_geolocation_dataset.csv")
order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
category_translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

datasets = {
    "customers": customers,
    "geolocation": geolocation,
    "order_items": order_items,
    "payments": payments,
    "reviews": reviews,
    "orders": orders,
    "products": products,
    "sellers": sellers,
    "category_translation": category_translation
}

print("Raw datasets loaded successfully.\n")

for name, df in datasets.items():
    print(f"{name}: {df.shape[0]:,} rows, {df.shape[1]} columns")


# %% Cell 3: Preview key datasets

print("Orders preview:")
print(orders.head())

print("\nOrder items preview:")
print(order_items.head())

print("\nPayments preview:")
print(payments.head())

print("\nReviews preview:")
print(reviews.head())

print("\nProducts preview:")
print(products.head())

# %% Cell 4: Check missing values in each dataset

print("Missing value check by dataset:")

for name, df in datasets.items():
    print(f"\n{name.upper()}")
    missing_values = df.isna().sum().sort_values(ascending=False)
    print(missing_values[missing_values > 0].head(10))

# Notes from missing value check:
# - Review comment fields have many missing values, but they are not needed for this dashboard.
# - Some orders have missing delivery dates, likely because they were canceled, unavailable, or not delivered.
# - Some products have missing category fields, which will be filled as "unknown" later.


# %% Cell 5: Checking type of date columns

orders[[
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]].dtypes

# %% Cell 6: Convert order date columns to datetime

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

print("Date columns converted successfully.\n")
print(orders[date_columns].dtypes)

# %% Cell 7: Aggregate payments to one row per order

payments_agg = (
    payments
    .groupby("order_id", as_index=False)
    .agg(order_payment_value=("payment_value", "sum"))
)

print("Original payments shape:", payments.shape)
print("Aggregated payments shape:", payments_agg.shape)

payments_agg.head()

# %% Cell 8: Aggregate reviews to one row per order

reviews_agg = (
    reviews
    .groupby("order_id", as_index=False)
    .agg(review_score=("review_score", "mean"))
)

print("Original reviews shape:", reviews.shape)
print("Aggregated reviews shape:", reviews_agg.shape)

reviews_agg.head()


# %% Cell 9: Translate product categories to English
# This step translates product categories from Portuguese to English.
# The products table contains product_category_name in Portuguese.
# The category_translation table maps each Portuguese category to an English category.
# A left join keeps all products, even if a translation is missing.
# The final product_category column is used in the dashboard for readable category analysis.

products = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

products["product_category"] = products["product_category_name_english"].fillna(
    products["product_category_name"]
)

print("Product categories translated successfully.")

products[[
    "product_id",
    "product_category_name",
    "product_category_name_english",
    "product_category"
]].head()


# %% Cell 10: Merge main dashboard dataset

# We start from order_items because this gives us one row per item sold.
# This is useful because one order can contain multiple products/sellers.

products_for_merge = products[[
    "product_id",
    "product_category"
]].drop_duplicates()

df = order_items.merge(orders, on="order_id", how="left")
print("After merging order_items + orders:", df.shape)

df = df.merge(customers, on="customer_id", how="left")
print("After merging customers:", df.shape)

df = df.merge(products_for_merge, on="product_id", how="left")
print("After merging products:", df.shape)

df = df.merge(sellers, on="seller_id", how="left")
print("After merging sellers:", df.shape)

df = df.merge(payments_agg, on="order_id", how="left")
print("After merging payments:", df.shape)

df = df.merge(reviews_agg, on="order_id", how="left")
print("After merging reviews:", df.shape)

df.head()


# %% Cell 11: Create dashboard calculation fields

# Item revenue is the listed product price plus freight/shipping value.
df["item_revenue"] = df["price"] + df["freight_value"]

# Calculate total item revenue per order.
# This is needed because one order can have multiple items.
df["order_item_total_revenue"] = df.groupby("order_id")["item_revenue"].transform("sum")

# Allocate the order payment value across order items.
# This prevents double-counting revenue when an order has multiple products.
df["payment_value"] = np.where(
    df["order_item_total_revenue"] > 0,
    df["order_payment_value"] * (df["item_revenue"] / df["order_item_total_revenue"]),
    df["item_revenue"]
)

# Calculate delivery time in days.
df["delivery_days"] = (
    df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
).dt.days

# Identify late deliveries.
# Only orders with actual delivery dates and estimated delivery dates are evaluated.
df["is_late_delivery"] = (
    df["order_delivered_customer_date"].notna()
    & df["order_estimated_delivery_date"].notna()
    & (df["order_delivered_customer_date"] > df["order_estimated_delivery_date"])
).astype(int)

# Create date fields for dashboard filtering and trend charts.
df["order_year"] = df["order_purchase_timestamp"].dt.year
df["order_month"] = df["order_purchase_timestamp"].dt.month
df["order_month_name"] = df["order_purchase_timestamp"].dt.strftime("%b")
df["order_year_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

df[[
    "order_id",
    "order_item_id",
    "price",
    "freight_value",
    "item_revenue",
    "order_payment_value",
    "payment_value",
    "delivery_days",
    "is_late_delivery",
    "order_year_month"
]].head()
# %% Cell 12: Create final dashboard-ready table

dashboard = df[[
    "order_id",
    "order_item_id",
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "seller_id",
    "seller_city",
    "seller_state",
    "product_id",
    "product_category",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "price",
    "freight_value",
    "item_revenue",
    "payment_value",
    "order_payment_value",
    "review_score",
    "is_late_delivery",
    "delivery_days",
    "order_month",
    "order_month_name",
    "order_year",
    "order_year_month"
]].copy()

dashboard = dashboard.rename(columns={
    "order_purchase_timestamp": "order_purchase_date"
})

# Handle missing values
dashboard["product_category"] = dashboard["product_category"].fillna("unknown")
dashboard["review_score"] = dashboard["review_score"].fillna(0)
dashboard["payment_value"] = dashboard["payment_value"].fillna(0)
dashboard["item_revenue"] = dashboard["item_revenue"].fillna(0)

print("Final dashboard table shape:", dashboard.shape)
print("Number of unique orders:", dashboard["order_id"].nunique())
print("Number of unique customers:", dashboard["customer_unique_id"].nunique())
print("Number of unique sellers:", dashboard["seller_id"].nunique())

dashboard.head()
# %% Cell 13: KPI sanity check

total_revenue = dashboard["payment_value"].sum()
total_orders = dashboard["order_id"].nunique()
average_order_value = total_revenue / total_orders
total_customers = dashboard["customer_unique_id"].nunique()
total_sellers = dashboard["seller_id"].nunique()

average_review_score = dashboard.loc[
    dashboard["review_score"] > 0,
    "review_score"
].mean()

# For late delivery rate, calculate at the order level instead of item level.
order_level_late_delivery = (
    dashboard
    .groupby("order_id", as_index=False)
    .agg(is_late_delivery=("is_late_delivery", "max"))
)

late_delivery_rate = order_level_late_delivery["is_late_delivery"].mean()

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: {average_order_value:,.2f}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Sellers: {total_sellers:,}")
print(f"Average Review Score: {average_review_score:.2f}")
print(f"Late Delivery Rate: {late_delivery_rate:.2%}")

# %% Cell 14: Final validation before export

print("Final validation checks\n")

print("Dashboard shape:", dashboard.shape)
print("Duplicate order item rows:", dashboard.duplicated(subset=["order_id", "order_item_id"]).sum())
print("Missing order IDs:", dashboard["order_id"].isna().sum())
print("Missing customer IDs:", dashboard["customer_id"].isna().sum())
print("Missing seller IDs:", dashboard["seller_id"].isna().sum())
print("Missing product IDs:", dashboard["product_id"].isna().sum())
print("Missing product categories:", dashboard["product_category"].isna().sum())
print("Missing payment values:", dashboard["payment_value"].isna().sum())
print("Negative payment values:", (dashboard["payment_value"] < 0).sum())
print("Negative price values:", (dashboard["price"] < 0).sum())
print("Negative freight values:", (dashboard["freight_value"] < 0).sum())

print("\nOrder status counts:")
print(dashboard["order_status"].value_counts())

print("\nDate range:")
print("First order date:", dashboard["order_purchase_date"].min())
print("Last order date:", dashboard["order_purchase_date"].max())

# %% Cell 15: Export dashboard-ready CSV

output_path = CLEAN_DIR / "dashboard_orders_summary.csv"

dashboard.to_csv(output_path, index=False)

print("Dashboard CSV created successfully.")
print("Output path:", output_path)
print(f"Rows exported: {len(dashboard):,}")
print(f"Columns exported: {len(dashboard.columns)}")
# %%
