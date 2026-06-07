@echo off
echo ========================================
echo   ANDES RETAIL DASHBOARD - Quick Start
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instala Python 3.8+ desde python.org
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [3/3] Iniciando Streamlit...
echo.
echo Tu dashboard estara disponible en: http://localhost:8501
echo Presiona Ctrl+C para detener el servidor
echo.

streamlit run streamlit_app.py
