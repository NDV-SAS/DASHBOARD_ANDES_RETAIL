#!/bin/bash

echo "========================================"
echo "  ANDES RETAIL DASHBOARD - Quick Start"
echo "========================================"
echo ""

echo "[1/3] Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no encontrado. Instala Python 3.8+"
    exit 1
fi

echo ""
echo "[2/3] Instalando dependencias..."
pip3 install -r requirements.txt

echo ""
echo "[3/3] Iniciando Streamlit..."
echo ""
echo "Tu dashboard estará disponible en: http://localhost:8501"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

streamlit run streamlit_app.py
