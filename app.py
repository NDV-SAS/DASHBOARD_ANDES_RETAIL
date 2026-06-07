import os
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from prepare_data import get_master_data
from calculate_kpis import calculate_all_kpis, get_monthly_sales, get_sales_by_region, get_sales_by_category

customers = pd.read_parquet("data/olist_customers_dataset.parquet")
order_items = pd.read_parquet("data/olist_order_items_dataset.parquet")
payments = pd.read_parquet("data/olist_order_payments_dataset.parquet")
reviews = pd.read_parquet("data/olist_order_reviews_dataset.parquet")
orders = pd.read_parquet("data/olist_orders_dataset.parquet")
products = pd.read_parquet("data/olist_products_dataset.parquet")
sellers = pd.read_parquet("data/olist_sellers_dataset.parquet")
categories = pd.read_parquet("data/product_category_name_translation.parquet")


app = Dash(__name__)

# Load data
df = get_master_data()
kpis = calculate_all_kpis()

# Get unique values for filters
states = sorted(df['customer_state'].dropna().unique())
categories = sorted(df['product_category_name_english'].dropna().unique())
statuses = sorted(df['order_status'].unique())
payment_types = sorted(df['payment_type'].dropna().unique())

# Warm color scheme
COLORS = ["#E85D04", "#DC2F02", "#F48C06", "#FFBA08", "#D00000"]
COLOR_SUCCESS = "#2A9D8F"
COLOR_WARNING = "#E76F51"
COLOR_DANGER = "#D62828"
COLOR_PRIMARY = "#E85D04"

app.layout = html.Div([
    html.Div([
        html.H1("DASHBOARD ESTRATÉGICO ANDES RETAIL", 
                style={'textAlign': 'center', 'marginBottom': '8px', 'fontSize': '34px', 'color': '#370617', 'fontWeight': '700'}),
        html.P("Ventas, rentabilidad, logística, experiencia del cliente y riesgo operativo",
               style={'textAlign': 'center', 'color': '#6C757D', 'marginTop': '0px', 'fontSize': '16px'})
    ], style={'padding': '25px 20px 15px 20px', 'backgroundColor': '#FFF8F0', 'borderBottom': '3px solid #E85D04'}),
    
    # Global Filters
    html.Div([
        html.Div([
            html.Label("Rango de Fechas", style={'fontWeight': 'bold', 'fontSize': '14px', 'color': '#370617', 'marginBottom': '5px', 'display': 'block'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['order_purchase_timestamp'].min(),
                end_date=df['order_purchase_timestamp'].max(),
                display_format='YYYY-MM-DD',
                style={'fontSize': '13px'}
            )
        ], style={'display': 'inline-block', 'marginRight': '25px', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Estado Cliente", style={'fontWeight': 'bold', 'fontSize': '14px', 'color': '#370617', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(id='state-filter', options=[{'label': 'Todos', 'value': 'ALL'}] + 
                        [{'label': s, 'value': s} for s in states],
                        value='ALL', clearable=False, style={'width': '160px', 'fontSize': '13px'})
        ], style={'display': 'inline-block', 'marginRight': '25px', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Categoría", style={'fontWeight': 'bold', 'fontSize': '14px', 'color': '#370617', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(id='category-filter', options=[{'label': 'Todas', 'value': 'ALL'}] + 
                        [{'label': c, 'value': c} for c in categories],
                        value='ALL', clearable=False, style={'width': '220px', 'fontSize': '13px'})
        ], style={'display': 'inline-block', 'marginRight': '25px', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Estado Pedido", style={'fontWeight': 'bold', 'fontSize': '14px', 'color': '#370617', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(id='status-filter', options=[{'label': 'Todos', 'value': 'ALL'}] + 
                        [{'label': s, 'value': s} for s in statuses],
                        value='ALL', clearable=False, style={'width': '160px', 'fontSize': '13px'})
        ], style={'display': 'inline-block', 'marginRight': '25px', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Medio de Pago", style={'fontWeight': 'bold', 'fontSize': '14px', 'color': '#370617', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(id='payment-filter', options=[{'label': 'Todos', 'value': 'ALL'}] + 
                        [{'label': p, 'value': p} for p in payment_types],
                        value='ALL', clearable=False, style={'width': '160px', 'fontSize': '13px'})
        ], style={'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'padding': '20px 25px', 'backgroundColor': '#fff', 'borderBottom': '2px solid #F4E5D3'}),
    
    # Navigation Tabs
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Resumen Ejecutivo', value='tab-1', 
                style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px'},
                selected_style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px', 'borderTop': '3px solid #E85D04', 'color': '#E85D04'}),
        dcc.Tab(label='Ventas y Rentabilidad', value='tab-2', 
                style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px'},
                selected_style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px', 'borderTop': '3px solid #E85D04', 'color': '#E85D04'}),
        dcc.Tab(label='Logística y Cumplimiento', value='tab-3', 
                style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px'},
                selected_style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px', 'borderTop': '3px solid #E85D04', 'color': '#E85D04'}),
        dcc.Tab(label='Clientes y Experiencia', value='tab-4', 
                style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px'},
                selected_style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px', 'borderTop': '3px solid #E85D04', 'color': '#E85D04'}),
        dcc.Tab(label='Categorías, Vendedores y Riesgo', value='tab-5', 
                style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px'},
                selected_style={'fontSize': '15px', 'fontWeight': '600', 'padding': '12px 24px', 'borderTop': '3px solid #E85D04', 'color': '#E85D04'})
    ], style={'marginTop': '0px'}),
    
    # Content
    html.Div(id='tab-content', style={'padding': '25px', 'backgroundColor': '#FFF8F0'})
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#FFF8F0', 'minHeight': '100vh'})


def filter_data(df, start_date, end_date, state, category, status, payment):
    """Apply filters to dataframe."""
    filtered = df.copy()
    
    if start_date and end_date:
        filtered = filtered[(filtered['order_purchase_timestamp'] >= start_date) & 
                           (filtered['order_purchase_timestamp'] <= end_date)]
    
    if state != 'ALL':
        filtered = filtered[filtered['customer_state'] == state]
    
    if category != 'ALL':
        filtered = filtered[filtered['product_category_name_english'] == category]
    
    if status != 'ALL':
        filtered = filtered[filtered['order_status'] == status]
    
    if payment != 'ALL':
        filtered = filtered[filtered['payment_type'] == payment]
    
    return filtered


def create_kpi_card(title, value, subtitle="", color="#E85D04", border_color="#E85D04"):
    """Create a KPI card with bold styling."""
    return html.Div([
        html.Div(title, style={'fontSize': '14px', 'color': '#6C757D', 'marginBottom': '8px', 'fontWeight': '700', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
        html.Div(value, style={'fontSize': '32px', 'fontWeight': '800', 'color': color, 'marginBottom': '5px', 'lineHeight': '1.2'}),
        html.Div(subtitle, style={'fontSize': '13px', 'color': '#6C757D', 'fontWeight': '500'})
    ], style={'padding': '20px', 'backgroundColor': '#fff', 'borderRadius': '8px', 
              'boxShadow': '0 4px 12px rgba(0,0,0,0.15)', 'margin': '8px',
              'borderLeft': f'5px solid {border_color}', 'transition': 'transform 0.2s'})


def apply_chart_theme(fig):
    """Apply warm theme to charts."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(size=13, color="#370617"),
        margin=dict(l=50, r=50, t=50, b=50),
        colorway=COLORS,
        xaxis=dict(automargin=True, gridcolor='#F4E5D3', showgrid=True),
        yaxis=dict(automargin=True, gridcolor='#F4E5D3', showgrid=True),
        title=dict(font=dict(size=18, color="#370617", family="Arial", weight=700))
    )
    return fig


@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('state-filter', 'value'),
     Input('category-filter', 'value'),
     Input('status-filter', 'value'),
     Input('payment-filter', 'value')]
)
def render_content(tab, start_date, end_date, state, category, status, payment):
    filtered_df = filter_data(df, start_date, end_date, state, category, status, payment)
    
    if len(filtered_df) == 0:
        return html.Div("No hay datos para los filtros seleccionados", 
                       style={'textAlign': 'center', 'padding': '60px', 'fontSize': '18px', 'color': '#6C757D', 'fontWeight': '600'})
    
    if tab == 'tab-1':
        return render_executive_summary(filtered_df)
    elif tab == 'tab-2':
        return render_sales_profitability(filtered_df)
    elif tab == 'tab-3':
        return render_logistics(filtered_df)
    elif tab == 'tab-4':
        return render_customer_experience(filtered_df)
    elif tab == 'tab-5':
        return render_categories_sellers(filtered_df)


def render_executive_summary(filtered_df):
    """Render Executive Summary tab."""
    delivered = filtered_df[filtered_df['order_status'] == 'delivered']
    
    # Calculate KPIs
    ventas_netas = filtered_df['price'].sum()
    ticket_promedio = filtered_df.groupby('order_id')['price'].sum().mean()
    tasa_cancelacion = filtered_df[filtered_df['canceled_flag'] == 1]['order_id'].nunique() / filtered_df['order_id'].nunique() if filtered_df['order_id'].nunique() > 0 else 0
    otif_pct = delivered['otif_flag'].mean() if len(delivered) > 0 else 0
    cantidad_vendida = len(filtered_df)
    unidades_por_venta = len(filtered_df) / filtered_df['order_id'].nunique() if filtered_df['order_id'].nunique() > 0 else 0
    entregas_tardias = delivered[delivered['late_delivery'] == 1]['order_id'].nunique() if len(delivered) > 0 else 0
    valor_cancelaciones = filtered_df[filtered_df['canceled_flag'] == 1]['price'].sum()
    
    # Determine OTIF color
    if otif_pct >= 0.95:
        otif_color = COLOR_SUCCESS
        otif_border = COLOR_SUCCESS
    elif otif_pct >= 0.80:
        otif_color = COLOR_WARNING
        otif_border = COLOR_WARNING
    else:
        otif_color = COLOR_DANGER
        otif_border = COLOR_DANGER
    
    # KPI Cards
    kpi_cards = html.Div([
        html.Div([
            create_kpi_card("Ventas Netas Totales", f"${ventas_netas:,.0f}", "Valor total vendido", COLOR_SUCCESS, COLOR_SUCCESS),
            create_kpi_card("Ticket Promedio", f"${ticket_promedio:,.2f}", "Valor promedio por pedido", COLOR_PRIMARY, COLOR_PRIMARY),
            create_kpi_card("Tasa de Cancelación", f"{tasa_cancelacion*100:.2f}%", "% pedidos cancelados", COLOR_DANGER, COLOR_DANGER),
            create_kpi_card("OTIF - Entregas a Tiempo", f"{otif_pct*100:.1f}%", "% entregas dentro de fecha prometida", otif_color, otif_border)
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '15px', 'marginBottom': '20px'}),
        
        html.Div([
            create_kpi_card("Cantidad Vendida", f"{cantidad_vendida:,}", "Unidades vendidas", "#F48C06", "#F48C06"),
            create_kpi_card("Unidades por Venta", f"{unidades_por_venta:.2f}", "Promedio unidades por pedido", "#FFBA08", "#FFBA08"),
            create_kpi_card("Entregas Tardías", f"{entregas_tardias:,}", "Pedidos entregados tarde", COLOR_DANGER, COLOR_DANGER),
            create_kpi_card("Valor Cancelaciones", f"${valor_cancelaciones:,.0f}", "Valor asociado a cancelaciones", COLOR_DANGER, COLOR_DANGER)
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '15px', 'marginBottom': '25px'})
    ])
    
    # Heatmap: Sales by Region and Category
    heatmap_data = filtered_df.groupby(['customer_state', 'product_category_name_english'])['price'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='customer_state', columns='product_category_name_english', values='price').fillna(0)
    
    # Limit to top 10 states and top 15 categories
    top_states = filtered_df.groupby('customer_state')['price'].sum().nlargest(10).index
    top_categories = filtered_df.groupby('product_category_name_english')['price'].sum().nlargest(15).index
    heatmap_pivot = heatmap_pivot.loc[heatmap_pivot.index.isin(top_states), heatmap_pivot.columns.isin(top_categories)]
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale=[[0, '#FFF8F0'], [0.25, '#FFBA08'], [0.5, '#F48C06'], [0.75, '#E85D04'], [1, '#DC2F02']],
        hovertemplate='Estado: %{y}<br>Categoría: %{x}<br>Ventas: $%{z:,.0f}<extra></extra>'
    ))
    fig_heatmap.update_layout(
        title="Mapa de Calor de Ventas por Región y Categoría",
        xaxis_title="Categoría",
        yaxis_title="Región / Estado",
        height=550
    )
    apply_chart_theme(fig_heatmap)
    
    return html.Div([
        kpi_cards,
        html.Div([dcc.Graph(figure=fig_heatmap)], 
                style={'backgroundColor': '#fff', 'borderRadius': '8px', 'padding': '15px', 
                       'boxShadow': '0 4px 12px rgba(0,0,0,0.15)'})
    ])


def render_sales_profitability(filtered_df):
    """Render Sales and Profitability tab."""
    # KPIs
    ventas_netas = filtered_df['price'].sum()
    valor_cancelaciones = filtered_df[filtered_df['canceled_flag'] == 1]['price'].sum()
    ingreso_neto_real = ventas_netas - valor_cancelaciones
    
    # Participation by Region
    region_sales = filtered_df.groupby('customer_state')['price'].sum().reset_index()
    region_sales['pct'] = region_sales['price'] / region_sales['price'].sum()
    region_sales = region_sales.sort_values('price', ascending=False).head(10)
    
    fig_region_pie = px.pie(region_sales, values='price', names='customer_state', 
                            title="Participación de Ventas por Región")
    apply_chart_theme(fig_region_pie)
    
    # Participation by Category - Treemap
    category_sales = filtered_df.groupby('product_category_name_english')['price'].sum().reset_index()
    category_sales = category_sales.sort_values('price', ascending=False).head(20)
    
    fig_category_tree = px.treemap(category_sales, path=['product_category_name_english'], values='price',
                                   title="Participación de Ventas por Categoría")
    apply_chart_theme(fig_category_tree)
    
    # Monthly Sales Growth
    monthly = filtered_df.groupby('year_month')['price'].sum().reset_index()
    monthly = monthly.sort_values('year_month')
    monthly['growth'] = monthly['price'].pct_change() * 100
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=monthly['year_month'], y=monthly['growth'], mode='lines+markers',
                                   name='Crecimiento %', line=dict(width=3, color='#E85D04'), 
                                   marker=dict(size=8, color='#DC2F02')))
    fig_growth.update_layout(title="Crecimiento Mensual de Ventas", xaxis_title="Mes", yaxis_title="Variación %")
    apply_chart_theme(fig_growth)
    
    # Margin by Region
    margin_data = filtered_df.groupby('customer_state').agg({
        'price': 'sum',
        'freight_value': 'sum'
    }).reset_index()
    margin_data['margin'] = ((margin_data['price'] - margin_data['freight_value']) / margin_data['price']) * 100
    margin_data = margin_data.sort_values('margin', ascending=False).head(15)
    
    fig_margin = px.bar(margin_data, x='customer_state', y='margin', 
                       title="Margen Neto Proxy por Región")
    fig_margin.update_layout(xaxis_title="Región", yaxis_title="% Margen Estimado")
    apply_chart_theme(fig_margin)
    
    # Category Ranking by Profitability
    category_profit = filtered_df.groupby('product_category_name_english').agg({
        'price': 'sum',
        'freight_value': 'sum'
    }).reset_index()
    category_profit['profit'] = category_profit['price'] - category_profit['freight_value']
    category_profit = category_profit.sort_values('profit', ascending=True).tail(15)
    
    fig_category_rank = px.bar(category_profit, x='profit', y='product_category_name_english', 
                              orientation='h', title="Ranking de Categorías por Rentabilidad Estimada")
    fig_category_rank.update_layout(xaxis_title="Rentabilidad Estimada", yaxis_title="Categoría")
    apply_chart_theme(fig_category_rank)
    
    # Pareto by Category
    pareto_data = filtered_df.groupby('product_category_name_english')['price'].sum().reset_index()
    pareto_data = pareto_data.sort_values('price', ascending=False).head(20)
    pareto_data['cumulative'] = pareto_data['price'].cumsum() / pareto_data['price'].sum() * 100
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=pareto_data['product_category_name_english'], y=pareto_data['price'], 
                               name='Ventas', yaxis='y', marker_color='#E85D04'))
    fig_pareto.add_trace(go.Scatter(x=pareto_data['product_category_name_english'], y=pareto_data['cumulative'],
                                   name='% Acumulado', yaxis='y2', mode='lines+markers',
                                   line=dict(width=3, color='#DC2F02'), marker=dict(size=8)))
    fig_pareto.update_layout(
        title="Pareto de Ventas por Categoría",
        xaxis_title="Categoría",
        yaxis=dict(title="Ventas"),
        yaxis2=dict(title="% Acumulado", overlaying='y', side='right'),
        hovermode='x unified'
    )
    apply_chart_theme(fig_pareto)
    
    kpi_cards = html.Div([
        create_kpi_card("Ingreso Neto Real", f"${ingreso_neto_real:,.0f}", "Ventas descontando cancelaciones", COLOR_SUCCESS, COLOR_SUCCESS),
        create_kpi_card("Ventas Netas", f"${ventas_netas:,.0f}", "Total vendido", COLOR_PRIMARY, COLOR_PRIMARY),
        create_kpi_card("Valor Cancelaciones", f"${valor_cancelaciones:,.0f}", "Pérdida por cancelaciones", COLOR_DANGER, COLOR_DANGER)
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '15px', 'marginBottom': '25px'})
    
    chart_style = {'backgroundColor': '#fff', 'borderRadius': '8px', 'padding': '15px', 
                   'boxShadow': '0 4px 12px rgba(0,0,0,0.15)', 'marginBottom': '20px'}
    
    return html.Div([
        kpi_cards,
        html.Div([
            html.Div([dcc.Graph(figure=fig_region_pie)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 10px 0 0'}),
            html.Div([dcc.Graph(figure=fig_category_tree)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 0 0 10px'})
        ], style=chart_style),
        html.Div([dcc.Graph(figure=fig_growth)], style=chart_style),
        html.Div([
            html.Div([dcc.Graph(figure=fig_margin)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 10px 0 0'}),
            html.Div([dcc.Graph(figure=fig_category_rank)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 0 0 10px'})
        ], style=chart_style),
        html.Div([dcc.Graph(figure=fig_pareto)], style=chart_style)
    ])


def render_logistics(filtered_df):
    """Render Logistics and Compliance tab."""
    delivered = filtered_df[filtered_df['order_status'] == 'delivered']
    
    if len(delivered) == 0:
        return html.Div("No hay pedidos entregados en el período seleccionado", 
                       style={'textAlign': 'center', 'padding': '60px', 'fontSize': '18px', 'color': '#6C757D'})
    
    # KPIs
    avg_delivery = delivered['delivery_days'].mean()
    late_orders = delivered[delivered['delay_days'] > 0]
    avg_delay = late_orders['delay_days'].mean() if len(late_orders) > 0 else 0
    otif_pct = delivered['otif_flag'].mean()
    
    # Distribution of Delivery Days
    fig_delivery_dist = px.histogram(delivered, x='delivery_days', nbins=30,
                                    title="Distribución de Días de Entrega")
    fig_delivery_dist.update_layout(xaxis_title="Días de Entrega", yaxis_title="Cantidad de Pedidos")
    fig_delivery_dist.update_traces(marker_color='#E85D04')
    apply_chart_theme(fig_delivery_dist)
    
    # Delay Distribution
    if len(late_orders) > 0:
        fig_delay_dist = px.histogram(late_orders, x='delay_days', nbins=20,
                                     title="Tiempo Promedio de Retraso")
        fig_delay_dist.update_layout(xaxis_title="Días de Retraso", yaxis_title="Número de Pedidos")
        fig_delay_dist.update_traces(marker_color='#DC2F02')
        apply_chart_theme(fig_delay_dist)
    else:
        fig_delay_dist = go.Figure()
        fig_delay_dist.add_annotation(text="No hay entregas tardías", showarrow=False, font=dict(size=16))
        apply_chart_theme(fig_delay_dist)
    
    # Late Deliveries by Region
    late_by_region = delivered[delivered['late_delivery'] == 1].groupby('customer_state').size().reset_index(name='count')
    late_by_region = late_by_region.sort_values('count', ascending=True).tail(15)
    
    fig_late_region = px.bar(late_by_region, x='count', y='customer_state', orientation='h',
                            title="Entregas Tardías por Región")
    fig_late_region.update_layout(xaxis_title="Número de Entregas Tardías", yaxis_title="Región")
    fig_late_region.update_traces(marker_color='#D62828')
    apply_chart_theme(fig_late_region)
    
    # OTIF by Region
    otif_by_region = delivered.groupby('customer_state')['otif_flag'].mean().reset_index()
    otif_by_region['otif_pct'] = otif_by_region['otif_flag'] * 100
    otif_by_region = otif_by_region.sort_values('otif_pct', ascending=False).head(15)
    
    fig_otif_region = px.bar(otif_by_region, x='customer_state', y='otif_pct',
                            title="OTIF por Región")
    fig_otif_region.update_layout(xaxis_title="Región", yaxis_title="% OTIF")
    fig_otif_region.update_traces(marker_color='#2A9D8F')
    apply_chart_theme(fig_otif_region)
    
    kpi_cards = html.Div([
        create_kpi_card("Tiempo Promedio de Entrega", f"{avg_delivery:.1f} días", "Días promedio", COLOR_PRIMARY, COLOR_PRIMARY),
        create_kpi_card("Tiempo Promedio de Retraso", f"{avg_delay:.1f} días", "Días de retraso", COLOR_DANGER, COLOR_DANGER),
        create_kpi_card("OTIF %", f"{otif_pct*100:.1f}%", "Entregas a tiempo", COLOR_SUCCESS, COLOR_SUCCESS)
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '15px', 'marginBottom': '25px'})
    
    chart_style = {'backgroundColor': '#fff', 'borderRadius': '8px', 'padding': '15px', 
                   'boxShadow': '0 4px 12px rgba(0,0,0,0.15)', 'marginBottom': '20px'}
    
    return html.Div([
        kpi_cards,
        html.Div([
            html.Div([dcc.Graph(figure=fig_delivery_dist)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 10px 0 0'}),
            html.Div([dcc.Graph(figure=fig_delay_dist)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 0 0 10px'})
        ], style=chart_style),
        html.Div([
            html.Div([dcc.Graph(figure=fig_late_region)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 10px 0 0'}),
            html.Div([dcc.Graph(figure=fig_otif_region)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 0 0 10px'})
        ], style=chart_style)
    ])


def render_customer_experience(filtered_df):
    """Render Customer Experience tab."""
    # KPIs
    avg_rating = filtered_df['review_score'].mean()
    
    # Rating Distribution
    rating_dist = filtered_df['review_score'].value_counts().sort_index().reset_index()
    rating_dist.columns = ['rating', 'count']
    
    fig_rating_dist = px.bar(rating_dist, x='rating', y='count',
                            title="Distribución de Calificaciones de Clientes")
    fig_rating_dist.update_layout(xaxis_title="Calificación", yaxis_title="Número de Pedidos")
    fig_rating_dist.update_traces(marker_color='#F48C06')
    apply_chart_theme(fig_rating_dist)
    
    # Delivery Time vs Rating
    delivered = filtered_df[filtered_df['order_status'] == 'delivered'].copy()
    if len(delivered) > 0:
        sample_size = min(5000, len(delivered))
        sample_df = delivered.sample(n=sample_size, random_state=42)
        
        fig_scatter = px.scatter(sample_df, x='delivery_days', y='review_score', 
                                color='customer_state', size='price',
                                title="Relación entre Tiempo de Entrega y Satisfacción")
        fig_scatter.update_layout(xaxis_title="Días de Entrega", yaxis_title="Calificación del Cliente")
        apply_chart_theme(fig_scatter)
    else:
        fig_scatter = go.Figure()
        apply_chart_theme(fig_scatter)
    
    # Rating by Category - Violin
    top_categories = filtered_df.groupby('product_category_name_english')['price'].sum().nlargest(15).index
    category_ratings = filtered_df[filtered_df['product_category_name_english'].isin(top_categories)]
    
    fig_violin = px.violin(category_ratings, x='product_category_name_english', y='review_score',
                          title="Variabilidad de Calificaciones por Categoría")
    fig_violin.update_layout(xaxis_title="Categoría", yaxis_title="Calificación")
    apply_chart_theme(fig_violin)
    
    kpi_cards = html.Div([
        create_kpi_card("Calificación Promedio del Cliente", f"{avg_rating:.2f}/5", "Review score promedio", COLOR_PRIMARY, COLOR_PRIMARY)
    ], style={'marginBottom': '25px'})
    
    chart_style = {'backgroundColor': '#fff', 'borderRadius': '8px', 'padding': '15px', 
                   'boxShadow': '0 4px 12px rgba(0,0,0,0.15)', 'marginBottom': '20px'}
    
    return html.Div([
        kpi_cards,
        html.Div([dcc.Graph(figure=fig_rating_dist)], style=chart_style),
        html.Div([dcc.Graph(figure=fig_scatter)], style=chart_style),
        html.Div([dcc.Graph(figure=fig_violin)], style=chart_style)
    ])


def render_categories_sellers(filtered_df):
    """Render Categories, Sellers and Risk tab."""
    # Payment Type Participation
    payment_dist = filtered_df.groupby('payment_type')['order_id'].nunique().reset_index()
    payment_dist.columns = ['payment_type', 'count']
    
    fig_payment = px.pie(payment_dist, values='count', names='payment_type',
                        title="Participación por Medio de Pago")
    apply_chart_theme(fig_payment)
    
    # Ticket by Payment Type
    ticket_by_payment = filtered_df.groupby('payment_type').apply(
        lambda x: x.groupby('order_id')['price'].sum().mean()
    ).reset_index()
    ticket_by_payment.columns = ['payment_type', 'avg_ticket']
    
    fig_ticket_payment = px.bar(ticket_by_payment, x='payment_type', y='avg_ticket',
                               title="Ticket Promedio por Medio de Pago")
    fig_ticket_payment.update_layout(xaxis_title="Medio de Pago", yaxis_title="Ticket Promedio")
    fig_ticket_payment.update_traces(marker_color='#FFBA08')
    apply_chart_theme(fig_ticket_payment)
    
    # Top Sellers
    seller_sales = filtered_df.groupby('seller_id')['price'].sum().reset_index()
    seller_sales = seller_sales.sort_values('price', ascending=True).tail(10)
    seller_sales['seller_name'] = 'Seller ' + seller_sales['seller_id'].str[:8]
    
    fig_sellers = px.bar(seller_sales, x='price', y='seller_name', orientation='h',
                        title="Top 10 Vendedores por Ventas")
    fig_sellers.update_layout(xaxis_title="Ventas", yaxis_title="Vendedor")
    fig_sellers.update_traces(marker_color='#E85D04')
    apply_chart_theme(fig_sellers)
    
    # Seller vs Customer State Flow
    flow_data = filtered_df.groupby(['seller_state', 'customer_state'])['price'].sum().reset_index()
    flow_pivot = flow_data.pivot(index='seller_state', columns='customer_state', values='price').fillna(0)
    
    # Limit to top states
    top_seller_states = filtered_df.groupby('seller_state')['price'].sum().nlargest(10).index
    top_customer_states = filtered_df.groupby('customer_state')['price'].sum().nlargest(10).index
    flow_pivot = flow_pivot.loc[flow_pivot.index.isin(top_seller_states), flow_pivot.columns.isin(top_customer_states)]
    
    fig_flow = go.Figure(data=go.Heatmap(
        z=flow_pivot.values,
        x=flow_pivot.columns,
        y=flow_pivot.index,
        colorscale=[[0, '#FFF8F0'], [0.25, '#FFBA08'], [0.5, '#F48C06'], [0.75, '#E85D04'], [1, '#DC2F02']],
        hovertemplate='Vendedor: %{y}<br>Cliente: %{x}<br>Ventas: $%{z:,.0f}<extra></extra>'
    ))
    fig_flow.update_layout(
        title="Flujo Comercial entre Vendedores y Clientes",
        xaxis_title="Estado del Cliente",
        yaxis_title="Estado del Vendedor",
        height=550
    )
    apply_chart_theme(fig_flow)
    
    # Strategic Matrix: Category vs Service
    delivered = filtered_df[filtered_df['order_status'] == 'delivered']
    if len(delivered) > 0:
        matrix_data = delivered.groupby('product_category_name_english').agg({
            'price': 'sum',
            'review_score': 'mean',
            'order_id': 'count',
            'otif_flag': 'mean'
        }).reset_index()
        matrix_data = matrix_data.nlargest(20, 'price')
        
        fig_matrix = px.scatter(matrix_data, x='price', y='review_score', size='order_id', 
                               color='otif_flag', hover_name='product_category_name_english',
                               title="Matriz Estratégica de Categorías",
                               color_continuous_scale=[[0, '#D62828'], [0.5, '#FFBA08'], [1, '#2A9D8F']])
        fig_matrix.update_layout(xaxis_title="Ventas Netas", yaxis_title="Calificación Promedio")
        apply_chart_theme(fig_matrix)
    else:
        fig_matrix = go.Figure()
        apply_chart_theme(fig_matrix)
    
    chart_style = {'backgroundColor': '#fff', 'borderRadius': '8px', 'padding': '15px', 
                   'boxShadow': '0 4px 12px rgba(0,0,0,0.15)', 'marginBottom': '20px'}
    
    return html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig_payment)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 10px 0 0'}),
            html.Div([dcc.Graph(figure=fig_ticket_payment)], style={'width': '50%', 'display': 'inline-block', 'padding': '0 0 0 10px'})
        ], style=chart_style),
        html.Div([dcc.Graph(figure=fig_sellers)], style=chart_style),
        html.Div([dcc.Graph(figure=fig_flow)], style=chart_style),
        html.Div([dcc.Graph(figure=fig_matrix)], style=chart_style)
    ])


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "localhost"), port=int(os.environ.get("PORT", "8050")))
