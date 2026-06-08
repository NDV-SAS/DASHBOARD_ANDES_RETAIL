import pandas as pd
import numpy as np
from pathlib import Path
from load_data import load_all_datasets

def prepare_master_dataset():
    """Merge all datasets and calculate derived metrics."""
    datasets = load_all_datasets()
    
    # Parse dates
    orders = datasets['orders'].copy()
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date',
                 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
    
    # Merge order_items with orders
    df = datasets['order_items'].merge(orders, on='order_id', how='left')
    
    # Merge customers
    df = df.merge(datasets['customers'], on='customer_id', how='left')
    
    # Merge products and categories
    products = datasets['products'].merge(datasets['categories'], 
                                         on='product_category_name', how='left')
    df = df.merge(products[['product_id', 'product_category_name', 'product_category_name_english']], 
                  on='product_id', how='left')
    
    # Merge sellers
    df = df.merge(datasets['sellers'], on='seller_id', how='left')
    
    # Merge payments (aggregate by order_id first)
    payments_agg = datasets['payments'].groupby('order_id').agg({
        'payment_type': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        'payment_value': 'sum'
    }).reset_index()
    df = df.merge(payments_agg, on='order_id', how='left')
    
    # Merge reviews
    reviews = datasets['reviews'][['order_id', 'review_score']].drop_duplicates('order_id')
    df = df.merge(reviews, on='order_id', how='left')
    
    # Calculate derived metrics
    df['total_order_value'] = df['price'] + df['freight_value']
    
    # Delivery days
    df['delivery_days'] = (df['order_delivered_customer_date'] - 
                           df['order_purchase_timestamp']).dt.days
    
    # Delay days
    df['delay_days'] = (df['order_delivered_customer_date'] - 
                        df['order_estimated_delivery_date']).dt.days
    
    # OTIF flag
    df['otif_flag'] = ((df['order_delivered_customer_date'] <= df['order_estimated_delivery_date']) & 
                       (df['order_status'] == 'delivered')).astype(int)
    
    # Late delivery flag
    df['late_delivery'] = (df['order_delivered_customer_date'] > 
                           df['order_estimated_delivery_date']).astype(int)
    
    # Canceled flag
    df['canceled_flag'] = (df['order_status'] == 'canceled').astype(int)
    
    # Extract date parts
    df['year'] = df['order_purchase_timestamp'].dt.year
    df['month'] = df['order_purchase_timestamp'].dt.month
    df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    return df

def get_master_data():
    """Get or create cached master dataset."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    cache_file = data_dir / "master_data.parquet"
    
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    else:
        df = prepare_master_dataset()
        df.to_parquet(cache_file, index=False)
        return df

def display():
    df = get_master_data()
    
    stats = [
        ("Total Rows", f"{len(df):,}"),
        ("Total Columns", f"{len(df.columns)}"),
        ("Date Range", f"{df['order_purchase_timestamp'].min().date()} to {df['order_purchase_timestamp'].max().date()}"),
        ("Unique Orders", f"{df['order_id'].nunique():,}"),
        ("Unique Customers", f"{df['customer_id'].nunique():,}"),
        ("Unique Products", f"{df['product_id'].nunique():,}"),
        ("Unique Sellers", f"{df['seller_id'].nunique():,}")
    ]
    
    return [
        {"_display_type": "stats", "stats": stats},
        {"title": "Master Dataset Sample", "df": df.head(20)},
        {"title": "Order Status Distribution", "df": df['order_status'].value_counts().reset_index()}
    ]

# --- Execute display() ---
"""Serializes and outputs the result of display() for the Plotly Studio runtime."""

import json
import traceback
