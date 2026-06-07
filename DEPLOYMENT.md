# Guía de Despliegue

## Opción 1: Despliegue en Streamlit Cloud (Recomendado)

### Paso 1: Preparar el Repositorio en GitHub

1. **Crear repositorio en GitHub:**
   ```bash
   cd andes_retail_dashboard
   git init
   git add .
   git commit -m "Initial commit: Andes Retail Dashboard"
   ```

2. **Crear repositorio en GitHub.com:**
   - Ve a https://github.com/new
   - Nombre: `andes-retail-dashboard`
   - Descripción: "Dashboard estratégico ejecutivo para análisis de retail"
   - Público o Privado (según preferencia)
   - NO inicializar con README (ya lo tienes)

3. **Conectar y subir:**
   ```bash
   git remote add origin https://github.com/TU_USUARIO/andes-retail-dashboard.git
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Desplegar en Streamlit Cloud

1. **Ir a Streamlit Cloud:**
   - Visita https://share.streamlit.io/
   - Inicia sesión con tu cuenta de GitHub

2. **Crear nueva app:**
   - Click en "New app"
   - Selecciona tu repositorio: `andes-retail-dashboard`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Esperar el despliegue:**
   - Streamlit Cloud instalará las dependencias automáticamente
   - El proceso toma 2-5 minutos
   - Una vez completado, recibirás una URL pública

### Paso 3: Configuración Adicional (Opcional)

**Configurar secretos (si necesitas):**
- En Streamlit Cloud, ve a Settings > Secrets
- Agrega variables de entorno en formato TOML

**Personalizar URL:**
- Settings > General > App URL
- Cambia el nombre de la app

**Configurar recursos:**
- Por defecto: 1 CPU, 800 MB RAM
- Para más recursos, considera Streamlit Cloud Pro

---

## Opción 2: Despliegue Local

### Ejecutar con Streamlit

```bash
cd andes_retail_dashboard
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Abre http://localhost:8501 en tu navegador.

### Ejecutar con Dash

```bash
cd andes_retail_dashboard
pip install -r requirements.txt
python app.py
```

Abre http://localhost:8050 en tu navegador.

---

## Opción 3: Despliegue en Render.com

1. **Crear cuenta en Render:**
   - Ve a https://render.com/
   - Regístrate con GitHub

2. **Crear Web Service:**
   - New > Web Service
   - Conecta tu repositorio GitHub
   - Configuración:
     - Name: `andes-retail-dashboard`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Desplegar:**
   - Click "Create Web Service"
   - Render desplegará automáticamente

---

## Opción 4: Despliegue en Heroku

1. **Crear Procfile:**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Crear setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Desplegar:**
   ```bash
   heroku login
   heroku create andes-retail-dashboard
   git push heroku main
   ```

---

## Solución de Problemas

### Error: "ModuleNotFoundError"
- Verifica que `requirements.txt` esté completo
- Ejecuta: `pip install -r requirements.txt`

### Error: "FileNotFoundError" para archivos CSV
- Asegúrate de que la carpeta `data/` esté en el repositorio
- Verifica que los archivos CSV estén en `data/`

### Dashboard muy lento
- Los datos son grandes (65 MB). Considera:
  - Usar solo una muestra de datos
  - Implementar caché más agresivo
  - Filtrar datos por fecha antes de cargar

### Límite de tamaño en GitHub
- GitHub tiene límite de 100 MB por archivo
- Si `olist_geolocation_dataset.csv` es muy grande, considera:
  - No incluirlo (no es esencial)
  - Usar Git LFS
  - Comprimir a .zip

---

## Optimizaciones para Producción

### 1. Reducir tamaño de datos

Crear versión filtrada de los datos:

```python
import pandas as pd

# Cargar solo últimos 12 meses
df = pd.read_csv('data/olist_orders_dataset.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df_recent = df[df['order_purchase_timestamp'] >= '2018-01-01']
df_recent.to_csv('data/olist_orders_dataset.csv', index=False)
```

### 2. Usar caché de Streamlit

Ya implementado en `streamlit_app.py`:
```python
@st.cache_data
def load_data():
    return get_master_data()
```

### 3. Comprimir archivos

```bash
# Comprimir CSVs a Parquet (más eficiente)
python -c "
import pandas as pd
from pathlib import Path

data_dir = Path('data')
for csv_file in data_dir.glob('*.csv'):
    df = pd.read_csv(csv_file)
    parquet_file = csv_file.with_suffix('.parquet')
    df.to_parquet(parquet_file, index=False)
    print(f'Converted {csv_file.name} to {parquet_file.name}')
"
```

---

## URLs de Ejemplo

Después del despliegue, tu dashboard estará disponible en:

- **Streamlit Cloud:** `https://TU_USUARIO-andes-retail-dashboard.streamlit.app`
- **Render:** `https://andes-retail-dashboard.onrender.com`
- **Heroku:** `https://andes-retail-dashboard.herokuapp.com`

---

## Mantenimiento

### Actualizar el dashboard

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de cambios"
git push origin main
```

Streamlit Cloud y Render redesplegarán automáticamente.

### Monitorear uso

- **Streamlit Cloud:** Dashboard > Analytics
- **Render:** Dashboard > Metrics
- **Heroku:** Dashboard > Metrics

---

## Soporte

Para problemas o preguntas:
- Streamlit: https://docs.streamlit.io/
- Render: https://render.com/docs
- Heroku: https://devcenter.heroku.com/
