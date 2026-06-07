import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prepare_data import get_master_data
from calculate_kpis import calculate_all_kpis

# Page config
st.set_page_config(
    page_title="Andes Retail Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for warm theme
st.markdown("""
<style>
    .main {
        background-color: #FFF8F0;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-left: 5px solid #E85D04;
    }
    .stMetric label {
        color: #6C757D;
        font-weight: 700;
        font-size: 14px;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #E85D04;
        font-size: 32px;
        font-weight: 800;
    }
    h1 {
        color: #370617;
        font-weight: 700;
    }
    h2, h3 {
        color: #370617;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return get_master_data()

df = load_data()

# Warm color scheme
COLORS = ["#E85D04", "#DC2F02", "#F48C06", "#FFBA08", "#D00000"]

def apply_chart_theme(fig):
    """Apply warm theme to charts."""
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(size=13, color="#370617"),
        colorway=COLORS,
        xaxis=dict(gridcolor='#F4E5D3', showgrid=True),
        yaxis=dict(gridcolor='#F4E5D3', showgrid=True)
    )
    return fig

# Header
st.title("📊 DASHBOARD ESTRATÉGICO ANDES RETAIL")
st.markdown("**Ventas, rentabilidad, logística, experiencia del cliente y riesgo operativo**")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filtros Globales")

# Date range
min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()
date_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# State filter
states = ['Todos'] + sorted(df['customer_state'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Estado Cliente", states)

# Category filter
categories = ['Todas'] + sorted(df['product_category_name_english'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Categoría", categories)

# Status filter
statuses = ['Todos'] + sorted(df['order_status'].unique().tolist())
selected_status = st.sidebar.selectbox("Estado Pedido", statuses)

# Payment filter
payment_types = ['Todos'] + sorted(df['payment_type'].dropna().unique().tolist())
selected_payment = st.sidebar.selectbox("Medio de Pago", payment_types)

# Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['order_purchase_timestamp'].dt.date >= start_date) &
        (filtered_df['order_purchase_timestamp'].dt.date <= end_date)
    ]

if selected_state != 'Todos':
    filtered_df = filtered_df[filtered_df['customer_state'] == selected_state]

if selected_category != 'Todas':
    filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]

if selected_status != 'Todos':
    filtered_df = filtered_df[filtered_df['order_status'] == selected_status]

if selected_payment != 'Todos':
    filtered_df = filtered_df[filtered_df['payment_type'] == selected_payment]

# Check if data exists
if len(filtered_df) == 0:
    st.warning("No hay datos para los filtros seleccionados")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Resumen Ejecutivo",
    "💰 Ventas y Rentabilidad",
    "🚚 Logística y Cumplimiento",
    "😊 Clientes y Experiencia",
    "🏪 Categorías, Vendedores y Riesgo"
])

# TAB 1: Executive Summary
with tab1:
    st.header("Resumen Ejecutivo")
    
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
    
    # KPI Cards - Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ventas Netas Totales", f"${ventas_netas:,.0f}", help="Valor total vendido")
    with col2:
        st.metric("Ticket Promedio", f"${ticket_promedio:,.2f}", help="Valor promedio por pedido")
    with col3:
        st.metric("Tasa de Cancelación", f"{tasa_cancelacion*100:.2f}%", help="% pedidos cancelados")
    with col4:
        st.metric("OTIF", f"{otif_pct*100:.1f}%", help="% entregas a tiempo")
    
    # KPI Cards - Row 2
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cantidad Vendida", f"{cantidad_vendida:,}", help="Unidades vendidas")
    with col2:
        st.metric("Unidades por Venta", f"{unidades_por_venta:.2f}", help="Promedio unidades por pedido")
    with col3:
        st.metric("Entregas Tardías", f"{entregas_tardias:,}", help="Pedidos entregados tarde")
    with col4:
        st.metric("Valor Cancelaciones", f"${valor_cancelaciones:,.0f}", help="Valor asociado a cancelaciones")
    
    st.markdown("---")
    
    # Heatmap
    st.subheader("Mapa de Calor de Ventas por Región y Categoría")
    heatmap_data = filtered_df.groupby(['customer_state', 'product_category_name_english'])['price'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='customer_state', columns='product_category_name_english', values='price').fillna(0)
    
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
    fig_heatmap.update_layout(height=500)
    apply_chart_theme(fig_heatmap)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# TAB 2: Sales and Profitability
with tab2:
    st.header("Ventas y Rentabilidad")
    
    ventas_netas = filtered_df['price'].sum()
    valor_cancelaciones = filtered_df[filtered_df['canceled_flag'] == 1]['price'].sum()
    ingreso_neto_real = ventas_netas - valor_cancelaciones
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ingreso Neto Real", f"${ingreso_neto_real:,.0f}", help="Ventas descontando cancelaciones")
    with col2:
        st.metric("Ventas Netas", f"${ventas_netas:,.0f}", help="Total vendido")
    with col3:
        st.metric("Valor Cancelaciones", f"${valor_cancelaciones:,.0f}", help="Pérdida por cancelaciones")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Participación de Ventas por Región")
        region_sales = filtered_df.groupby('customer_state')['price'].sum().reset_index()
        region_sales = region_sales.sort_values('price', ascending=False).head(10)
        fig_region = px.pie(region_sales, values='price', names='customer_state')
        apply_chart_theme(fig_region)
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        st.subheader("Participación de Ventas por Categoría")
        category_sales = filtered_df.groupby('product_category_name_english')['price'].sum().reset_index()
        category_sales = category_sales.sort_values('price', ascending=False).head(20)
        fig_category = px.treemap(category_sales, path=['product_category_name_english'], values='price')
        apply_chart_theme(fig_category)
        st.plotly_chart(fig_category, use_container_width=True)
    
    st.subheader("Crecimiento Mensual de Ventas")
    monthly = filtered_df.groupby('year_month')['price'].sum().reset_index()
    monthly = monthly.sort_values('year_month')
    monthly['growth'] = monthly['price'].pct_change() * 100
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=monthly['year_month'], y=monthly['growth'], mode='lines+markers',
                                   line=dict(width=3, color='#E85D04'), marker=dict(size=8, color='#DC2F02')))
    fig_growth.update_layout(xaxis_title="Mes", yaxis_title="Variación %")
    apply_chart_theme(fig_growth)
    st.plotly_chart(fig_growth, use_container_width=True)

# TAB 3: Logistics
with tab3:
    st.header("Logística y Cumplimiento")
    
    delivered = filtered_df[filtered_df['order_status'] == 'delivered']
    
    if len(delivered) > 0:
        avg_delivery = delivered['delivery_days'].mean()
        late_orders = delivered[delivered['delay_days'] > 0]
        avg_delay = late_orders['delay_days'].mean() if len(late_orders) > 0 else 0
        otif_pct = delivered['otif_flag'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tiempo Promedio de Entrega", f"{avg_delivery:.1f} días")
        with col2:
            st.metric("Tiempo Promedio de Retraso", f"{avg_delay:.1f} días")
        with col3:
            st.metric("OTIF %", f"{otif_pct*100:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Días de Entrega")
            fig_delivery = px.histogram(delivered, x='delivery_days', nbins=30)
            fig_delivery.update_traces(marker_color='#E85D04')
            apply_chart_theme(fig_delivery)
            st.plotly_chart(fig_delivery, use_container_width=True)
        
        with col2:
            st.subheader("OTIF por Región")
            otif_by_region = delivered.groupby('customer_state')['otif_flag'].mean().reset_index()
            otif_by_region['otif_pct'] = otif_by_region['otif_flag'] * 100
            otif_by_region = otif_by_region.sort_values('otif_pct', ascending=False).head(15)
            fig_otif = px.bar(otif_by_region, x='customer_state', y='otif_pct')
            fig_otif.update_traces(marker_color='#2A9D8F')
            apply_chart_theme(fig_otif)
            st.plotly_chart(fig_otif, use_container_width=True)
    else:
        st.warning("No hay pedidos entregados en el período seleccionado")

# TAB 4: Customer Experience
with tab4:
    st.header("Clientes y Experiencia")
    
    avg_rating = filtered_df['review_score'].mean()
    
    st.metric("Calificación Promedio del Cliente", f"{avg_rating:.2f}/5")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Calificaciones")
        rating_dist = filtered_df['review_score'].value_counts().sort_index().reset_index()
        rating_dist.columns = ['rating', 'count']
        fig_rating = px.bar(rating_dist, x='rating', y='count')
        fig_rating.update_traces(marker_color='#F48C06')
        apply_chart_theme(fig_rating)
        st.plotly_chart(fig_rating, use_container_width=True)
    
    with col2:
        st.subheader("Variabilidad por Categoría")
        top_categories = filtered_df.groupby('product_category_name_english')['price'].sum().nlargest(10).index
        category_ratings = filtered_df[filtered_df['product_category_name_english'].isin(top_categories)]
        fig_violin = px.violin(category_ratings, x='product_category_name_english', y='review_score')
        apply_chart_theme(fig_violin)
        st.plotly_chart(fig_violin, use_container_width=True)

# TAB 5: Categories and Sellers
with tab5:
    st.header("Categorías, Vendedores y Riesgo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Participación por Medio de Pago")
        payment_dist = filtered_df.groupby('payment_type')['order_id'].nunique().reset_index()
        payment_dist.columns = ['payment_type', 'count']
        fig_payment = px.pie(payment_dist, values='count', names='payment_type')
        apply_chart_theme(fig_payment)
        st.plotly_chart(fig_payment, use_container_width=True)
    
    with col2:
        st.subheader("Ticket Promedio por Medio de Pago")
        ticket_by_payment = filtered_df.groupby('payment_type').apply(
            lambda x: x.groupby('order_id')['price'].sum().mean()
        ).reset_index()
        ticket_by_payment.columns = ['payment_type', 'avg_ticket']
        fig_ticket = px.bar(ticket_by_payment, x='payment_type', y='avg_ticket')
        fig_ticket.update_traces(marker_color='#FFBA08')
        apply_chart_theme(fig_ticket)
        st.plotly_chart(fig_ticket, use_container_width=True)
    
    st.subheader("Top 10 Vendedores por Ventas")
    seller_sales = filtered_df.groupby('seller_id')['price'].sum().reset_index()
    seller_sales = seller_sales.sort_values('price', ascending=True).tail(10)
    seller_sales['seller_name'] = 'Seller ' + seller_sales['seller_id'].str[:8]
    fig_sellers = px.bar(seller_sales, x='price', y='seller_name', orientation='h')
    fig_sellers.update_traces(marker_color='#E85D04')
    apply_chart_theme(fig_sellers)
    st.plotly_chart(fig_sellers, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Dashboard Estratégico Andes Retail** | Datos: Olist Brazilian E-Commerce")
