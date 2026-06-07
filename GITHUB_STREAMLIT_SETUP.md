# 🚀 Instrucciones para Publicar en GitHub y Streamlit

## ✅ Paso 1: Verificar el Paquete

Tu proyecto está listo en:
```
C:\Users\godoy\AppData\Roaming\com.plotly.studio\sessions\b5b0d273-a08a-4943-88a5-347e370a3b5d\andes_retail_dashboard
```

Contenido:
- ✓ 5 archivos Python (app.py, streamlit_app.py, etc.)
- ✓ 8 archivos de datos CSV (62 MB)
- ✓ README.md y DEPLOYMENT.md
- ✓ requirements.txt
- ✓ .gitignore y .gitattributes

---

## 📦 Paso 2: Inicializar Git y Subir a GitHub

### 2.1 Abrir Terminal en el Proyecto

```bash
cd "C:\Users\godoy\AppData\Roaming\com.plotly.studio\sessions\b5b0d273-a08a-4943-88a5-347e370a3b5d\andes_retail_dashboard"
```

### 2.2 Inicializar Git

```bash
git init
git add .
git commit -m "Initial commit: Andes Retail Strategic Dashboard"
```

### 2.3 Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Configuración:
   - **Repository name:** `andes-retail-dashboard`
   - **Description:** `Dashboard estratégico ejecutivo para análisis de ventas, rentabilidad, logística y experiencia del cliente`
   - **Visibility:** Public (para usar Streamlit Cloud gratis)
   - **NO marcar:** "Initialize this repository with a README"
3. Click "Create repository"

### 2.4 Conectar y Subir

Copia los comandos que GitHub te muestra, o usa estos (reemplaza TU_USUARIO):

```bash
git remote add origin https://github.com/TU_USUARIO/andes-retail-dashboard.git
git branch -M main
git push -u origin main
```

**Nota:** Si es tu primera vez, Git te pedirá autenticación:
- Usuario: tu nombre de usuario de GitHub
- Contraseña: usa un Personal Access Token (no tu contraseña)
  - Crear token: https://github.com/settings/tokens
  - Scopes necesarios: `repo`

---

## 🌐 Paso 3: Desplegar en Streamlit Cloud

### 3.1 Crear Cuenta en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Click "Sign up" o "Sign in"
3. Selecciona "Continue with GitHub"
4. Autoriza Streamlit Cloud a acceder a tus repositorios

### 3.2 Crear Nueva App

1. En Streamlit Cloud, click "New app"
2. Configuración:
   - **Repository:** `TU_USUARIO/andes-retail-dashboard`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL (opcional):** `andes-retail` (personaliza la URL)

3. Click "Deploy!"

### 3.3 Esperar el Despliegue

- Streamlit instalará las dependencias (2-5 minutos)
- Verás logs en tiempo real
- Una vez completado, tu app estará en:
  ```
  https://TU_USUARIO-andes-retail.streamlit.app
  ```

---

## ⚠️ Consideraciones Importantes

### Tamaño de los Datos (62 MB)

Los archivos CSV son grandes. Opciones:

**Opción A: Subir todo (más fácil)**
- GitHub permite hasta 100 MB por archivo
- Tus archivos más grandes:
  - `olist_orders_dataset.csv`: 17 MB ✓
  - `olist_order_items_dataset.csv`: 15 MB ✓
  - `olist_order_reviews_dataset.csv`: 14 MB ✓
- Todos están bajo el límite, así que puedes subirlos directamente

**Opción B: Usar Git LFS (si tienes problemas)**
```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes
git commit -m "Configure Git LFS"
git push
```

**Opción C: Reducir datos (para mejor rendimiento)**
```bash
# Filtrar solo últimos 12 meses
python -c "
import pandas as pd
df = pd.read_csv('data/olist_orders_dataset.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df_recent = df[df['order_purchase_timestamp'] >= '2018-01-01']
df_recent.to_csv('data/olist_orders_dataset.csv', index=False)
print(f'Reducido a {len(df_recent):,} filas')
"
```

### Límites de Streamlit Cloud (Plan Gratuito)

- **Recursos:** 1 CPU, 800 MB RAM
- **Tiempo de inactividad:** La app se apaga después de 7 días sin uso
- **Límite de apps:** 1 app pública gratis

Si necesitas más recursos, considera:
- Streamlit Cloud Pro ($20/mes)
- Render.com (gratis con límites)
- Railway.app (gratis con límites)

---

## 🔧 Solución de Problemas

### Error: "File size exceeds GitHub's limit"

Si algún archivo supera 100 MB:
```bash
# Opción 1: Excluir el archivo
echo "data/archivo_grande.csv" >> .gitignore
git rm --cached data/archivo_grande.csv
git commit -m "Remove large file"

# Opción 2: Usar Git LFS
git lfs install
git lfs track "data/archivo_grande.csv"
git add .gitattributes data/archivo_grande.csv
git commit -m "Add large file with LFS"
```

### Error: "ModuleNotFoundError" en Streamlit

Verifica `requirements.txt`:
```bash
cat requirements.txt
```

Debe contener:
```
dash==2.14.2
plotly==5.18.0
pandas==2.1.4
numpy==1.26.2
streamlit==1.29.0
pyarrow==14.0.1
```

### App muy lenta en Streamlit

1. **Reducir datos:** Filtra solo datos recientes
2. **Optimizar caché:** Ya implementado con `@st.cache_data`
3. **Usar Parquet:** Más eficiente que CSV
   ```bash
   python -c "
   import pandas as pd
   from pathlib import Path
   for csv in Path('data').glob('*.csv'):
       df = pd.read_csv(csv)
       df.to_parquet(csv.with_suffix('.parquet'))
   "
   ```
   Luego actualiza `load_data.py` para leer `.parquet`

### Error de autenticación en Git

Si `git push` falla:
1. Crea un Personal Access Token: https://github.com/settings/tokens
2. Scopes: `repo`
3. Copia el token
4. Úsalo como contraseña cuando Git lo pida

O configura SSH:
```bash
ssh-keygen -t ed25519 -C "tu_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Copia la clave y agrégala en GitHub Settings > SSH Keys
```

---

## 📊 Verificar el Despliegue

Una vez desplegado, verifica:

1. **Filtros funcionan:** Cambia fecha, región, categoría
2. **KPIs se actualizan:** Los números cambian con los filtros
3. **Gráficos cargan:** Todas las visualizaciones aparecen
4. **Navegación funciona:** Las 5 pestañas se abren correctamente

---

## 🎉 ¡Listo!

Tu dashboard estará disponible públicamente en:
```
https://TU_USUARIO-andes-retail.streamlit.app
```

Comparte el link con tu equipo o clientes.

---

## 📝 Próximos Pasos (Opcional)

1. **Personalizar dominio:** Streamlit Cloud Pro permite dominios personalizados
2. **Agregar autenticación:** Proteger con contraseña
3. **Configurar CI/CD:** Auto-deploy en cada commit
4. **Monitorear uso:** Ver analytics en Streamlit Cloud
5. **Optimizar rendimiento:** Implementar más caché, reducir datos

---

## 📞 Soporte

- **Streamlit Docs:** https://docs.streamlit.io/
- **GitHub Docs:** https://docs.github.com/
- **Comunidad Streamlit:** https://discuss.streamlit.io/

¡Buena suerte con tu dashboard! 🚀
