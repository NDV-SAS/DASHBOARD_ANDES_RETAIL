import pandas as pd
import numpy as np
from prepare_data import get_master_data

def calculate_all_kpis():
    """Calculate all 38 KPIs for the dashboard."""
    df = get_master_data()
    
    # Filter to delivered orders for most metrics
    delivered = df[df['order_status'] == 'delivered'].copy()
    
    kpis = {}
    
    # KPI 1: Ventas Netas
    kpis['ventas_netas'] = df['price'].sum()
    
    # KPI 2: Ticket Promedio
    kpis['ticket_promedio'] = df.groupby('order_id')['price'].sum().mean()
    
    # KPI 3: Tasa de Cancelación
    kpis['tasa_cancelacion'] = (df[df['canceled_flag'] == 1]['order_id'].nunique() / 
                                 df['order_id'].nunique())
    
    # KPI 4: OTIF %
    kpis['otif_pct'] = delivered['otif_flag'].mean()
    
    # KPI 5: Cantidad Vendida
    kpis['cantidad_vendida'] = len(df)
    
    # KPI 6: Unidades por Venta
    kpis['unidades_por_venta'] = len(df) / df['order_id'].nunique()
    
    # KPI 7: Entregas Tardías
    kpis['entregas_tardias'] = delivered[delivered['late_delivery'] == 1]['order_id'].nunique()
    
    # KPI 8: Valor Cancelaciones
    kpis['valor_cancelaciones'] = df[df['canceled_flag'] == 1]['price'].sum()
    
    # KPI 9: Ingreso Neto Real
    kpis['ingreso_neto_real'] = kpis['ventas_netas'] - kpis['valor_cancelaciones']
    
    # KPI 17: Tiempo Promedio de Entrega
    kpis['tiempo_promedio_entrega'] = delivered['delivery_days'].mean()
    
    # KPI 18: Tiempo Promedio de Retraso
    late_orders = delivered[delivered['delay_days'] > 0]
    kpis['tiempo_promedio_retraso'] = late_orders['delay_days'].mean() if len(late_orders) > 0 else 0
    
    # KPI 24: Calificación Promedio
    kpis['calificacion_promedio'] = df['review_score'].mean()
    
    # KPI 28: Índice de Recompra
    customer_orders = df.groupby('customer_id')['order_id'].nunique()
    kpis['indice_recompra'] = (customer_orders > 1).sum() / len(customer_orders)
    
    return kpis

def get_monthly_sales():
    """Get monthly sales data."""
    df = get_master_data()
    monthly = df.groupby('year_month').agg({
        'price': 'sum',
        'order_id': 'nunique',
        'canceled_flag': 'sum'
    }).reset_index()
    monthly.columns = ['year_month', 'sales', 'orders', 'canceled']
    monthly = monthly.sort_values('year_month')
    return monthly

def get_sales_by_region():
    """Get sales by customer state."""
    df = get_master_data()
    by_region = df.groupby('customer_state').agg({
        'price': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    by_region.columns = ['state', 'sales', 'orders']
    by_region = by_region.sort_values('sales', ascending=False)
    return by_region

def get_sales_by_category():
    """Get sales by product category."""
    df = get_master_data()
    by_category = df.groupby('product_category_name_english').agg({
        'price': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    by_category.columns = ['category', 'sales', 'orders']
    by_category = by_category.sort_values('sales', ascending=False)
    return by_category

def display():
    kpis = calculate_all_kpis()
    
    stats = [
        ("Ventas Netas", f"${kpis['ventas_netas']:,.0f}"),
        ("Ticket Promedio", f"${kpis['ticket_promedio']:,.2f}"),
        ("OTIF %", f"{kpis['otif_pct']*100:.1f}%"),
        ("Tasa Cancelación", f"{kpis['tasa_cancelacion']*100:.2f}%"),
        ("Entregas Tardías", f"{kpis['entregas_tardias']:,}"),
        ("Tiempo Entrega (días)", f"{kpis['tiempo_promedio_entrega']:.1f}"),
        ("Calificación Promedio", f"{kpis['calificacion_promedio']:.2f}/5"),
        ("Índice Recompra", f"{kpis['indice_recompra']*100:.1f}%")
    ]
    
    monthly = get_monthly_sales()
    by_region = get_sales_by_region()
    by_category = get_sales_by_category()
    
    return [
        {"_display_type": "stats", "stats": stats},
        {"title": "Monthly Sales", "df": monthly.head(20)},
        {"title": "Top 10 Regions", "df": by_region.head(10)},
        {"title": "Top 10 Categories", "df": by_category.head(10)}
    ]

# --- Execute display() ---
"""Serializes and outputs the result of display() for the Plotly Studio runtime."""

import json
import traceback

from utils.display_util import _dumps, _serialize_result  # type: ignore[import-not-found]

if __name__ == "__main__":
    try:
        if "display" in dir():
            _result = display()  # type: ignore[name-defined]  # noqa: F821 - defined in user code
        else:
            # Fallback for data modules that define classes/functions but no display().
            # Just report success so the step doesn't error out.
            _result = {
                "_display_type": "stats",
                "stats": [("Status", "Module loaded successfully")],
            }
        _serialized = _serialize_result(_result)
        _json_str = _dumps(_serialized)
    except Exception as _display_err:
        _json_str = json.dumps({"type": "error", "value": traceback.format_exc()})
    print("__RESULT_START__")
    print(_json_str)
    print("__RESULT_END__")
