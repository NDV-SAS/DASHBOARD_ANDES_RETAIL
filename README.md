# Andes Retail Strategic Dashboard

Dashboard estratégico ejecutivo para análisis de ventas, rentabilidad, logística, experiencia del cliente y riesgo operativo.

## Características

- **5 páginas interactivas** con 38 KPIs
- **Filtros globales**: fecha, región, categoría, estado de pedido, medio de pago
- **Visualizaciones**: mapas de calor, gráficos de tendencias, análisis Pareto, matrices estratégicas
- **Tema visual cálido** con diseño ejecutivo

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Dash (aplicación web completa)

```bash
python app.py
```

Abre http://localhost:8050 en tu navegador.

### Streamlit (versión alternativa)

```bash
streamlit run streamlit_app.py
```

## Estructura del Proyecto

```
andes_retail_dashboard/
├── data/                          # Datasets Olist
├── app.py                         # Aplicación Dash principal
├── streamlit_app.py              # Aplicación Streamlit
├── prepare_data.py               # Preparación y limpieza de datos
├── calculate_kpis.py             # Cálculo de KPIs
├── requirements.txt              # Dependencias Python
└── README.md                     # Este archivo
```

## KPIs Principales

### Resumen Ejecutivo
- Ventas Netas Totales
- Ticket Promedio
- Tasa de Cancelación
- OTIF (On-Time In-Full)
- Cantidad Vendida
- Unidades por Venta
- Entregas Tardías
- Valor Cancelaciones

### Ventas y Rentabilidad
- Ingreso Neto Real
- Participación por Región
- Participación por Categoría
- Crecimiento Mensual
- Margen Neto Proxy
- Ranking de Categorías
- Análisis Pareto

### Logística y Cumplimiento
- Tiempo Promedio de Entrega
- Tiempo Promedio de Retraso
- Distribución de Días de Entrega
- Entregas Tardías por Región
- OTIF por Región

### Clientes y Experiencia
- Calificación Promedio
- Distribución de Calificaciones
- Relación Tiempo-Satisfacción
- Variabilidad por Categoría

### Categorías, Vendedores y Riesgo
- Participación por Medio de Pago
- Ticket por Medio de Pago
- Top Vendedores
- Flujo Comercial
- Matriz Estratégica

## Datos

Los datos provienen del dataset público **Olist Brazilian E-Commerce** que contiene información de pedidos, clientes, productos, vendedores y reviews del marketplace brasileño.

## Tecnologías

- **Dash**: Framework web interactivo
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **Streamlit**: Alternativa para deployment rápido

## Licencia

MIT License
