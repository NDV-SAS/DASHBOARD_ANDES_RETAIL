import pandas as pd
from pathlib import Path

def load_all_datasets():
    """Load all Olist datasets."""
    uploads = Path(__file__).parent / "uploads"
    
    orders = pd.read_csv(uploads / "olist_orders_dataset.csv")
    order_items = pd.read_csv(uploads / "olist_order_items_dataset.csv")
    payments = pd.read_csv(uploads / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(uploads / "olist_order_reviews_dataset.csv")
    customers = pd.read_csv(uploads / "olist_customers_dataset.csv")
    products = pd.read_csv(uploads / "olist_products_dataset.csv")
    sellers = pd.read_csv(uploads / "olist_sellers_dataset.csv")
    categories = pd.read_csv(uploads / "product_category_name_translation.csv")
    
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

# --- Execute display() ---
"""Serializes and outputs the result of display() for the Plotly Studio runtime."""

#import json
#import traceback

#from utils.display_util import _dumps, _serialize_result  # type: ignore[import-not-found]

#if __name__ == "__main__":
#    try:
#        if "display" in dir():
#           _result = display()  # type: ignore[name-defined]  # noqa: F821 - defined in user code
#        else:
#            # Fallback for data modules that define classes/functions but no display().
#            # Just report success so the step doesn't error out.
#            _result = {
#                "_display_type": "stats",
#                "stats": [("Status", "Module loaded successfully")],
#            }
#        _serialized = _serialize_result(_result)
#        _json_str = _dumps(_serialized)
#    except Exception as _display_err:
#        _json_str = json.dumps({"type": "error", "value": traceback.format_exc()})
#    print("__RESULT_START__")
#    print(_json_str)
#    print("__RESULT_END__")
