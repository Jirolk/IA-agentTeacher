@echo off
title ADI - Asistente Docente Inteligente
echo Cargando ADI... Por favor, espere un momento.

:: Cambiar al directorio donde esta el archivo .bat
cd /d "%~dp0"

:: Verificar si existe la carpeta venv, si no, crearla e instalar
if not exist venv (
    echo Configurando por primera vez... esto tardara unos minutos.
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

:: Iniciar Streamlit en segundo plano y abrir navegador
echo Abriendo ADI en su navegador...
start "" http://localhost:8501
streamlit run app/main.py --server.port 8501 --server.headless true
pause
