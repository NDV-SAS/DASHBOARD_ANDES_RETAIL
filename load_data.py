import pandas as pd
from pathlib import Path

def load_all_datasets():
    """Load all Olist datasets."""
    
    data = Path(__file__).parent / "data"

    orders = pd.read_parquet(data / "olist_orders_dataset.parquet")
    order_items = pd.read_parquet(data / "olist_order_items_dataset.parquet")
    payments = pd.read_parquet(data / "olist_order_payments_dataset.parquet")
    reviews = pd.read_parquet(data / "olist_order_reviews_dataset.parquet")
    customers = pd.read_parquet(data / "olist_customers_dataset.parquet")
    products = pd.read_parquet(data / "olist_products_dataset.parquet")
    sellers = pd.read_parquet(data / "olist_sellers_dataset.parquet")
    categories = pd.read_parquet(data / "product_category_name_translation.parquet")
        
    return {
        'orders': orders,
        'order_items': order_items,
        'payments': payments,
        'reviews': reviews,
        'customers': customers,
        'products': products,
        'sellers': sellers,
        'categories': categories
    }

def display():
    datasets = load_all_datasets()
    
    stats = []
    for name, df in datasets.items():
        stats.append((name, f"{len(df):,} rows, {len(df.columns)} cols"))
    
    orders = datasets['orders']
    
    return [
        {"_display_type": "stats", "stats": stats},
        {"title": "Orders Sample", "df": orders.head(20)},
        {"title": "Orders Columns", "df": pd.DataFrame({
            'Column': orders.columns,
            'Type': orders.dtypes.values,
            'Non-Null': orders.count().values
        })}
    ]

