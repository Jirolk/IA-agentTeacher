import streamlit as st
import json
import os
import sys
import logging
from datetime import datetime
import subprocess

# Configuración de rutas para que funcione desde cualquier lugar (.vbs o .bat)
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directorio_app = os.path.join(directorio_raiz, 'app')

if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)
if directorio_app not in sys.path:
    sys.path.append(directorio_app)

# Importar funciones locales de forma directa
from motor_ia import transcribir_audio, procesar_peticion_texto
from file_utils import generar_word_planeamiento, actualizar_nota_excel, leer_texto_word, eliminar_archivo

# --- FUNCIONES DE ACTUALIZACIÓN ---
def buscar_actualizaciones():
    try:
        # Ejecutamos git pull para traer cambios
        resultado = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        if "Already up to date" in resultado.stdout:
            return "✅ El sistema ya está actualizado.", False
        else:
            # Si hubo cambios, intentamos actualizar librerías por si acaso
            subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True)
            return f"🚀 ¡Sistema actualizado con éxito! Reanudando...", True
    except Exception as e:
        return f"❌ Error al actualizar: {str(e)}", False

# Configuración de Logging para DEBUG
logging.basicConfig(
    filename='debug_adi.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.set_page_config(page_title="ADI - Tu Asistente Docente", page_icon="👩‍🏫", layout="wide")

# --- FUNCIONES DE GESTIÓN ---
def listar_archivos(carpeta="data/output"):
    if not os.path.exists(carpeta):
        return []
    # Ordenamos por fecha de modificación para que los más nuevos salgan arriba
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".docx")]
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta, x)), reverse=True)
    return archivos

@st.dialog("📝 Revisando el Plan de Clase")
def mostrar_plan_modal(ruta, nombre):
    st.write(f"**Archivo:** {nombre}")
    texto_preview = leer_texto_word(ruta)
    st.text_area("Contenido del documento:", texto_preview, height=400)
    
    col1, col2 = st.columns(2)
    with col1:
        with open(ruta, "rb") as f:
            st.download_button("📥 GUARDAR EN MI PC", f, file_name=nombre, use_container_width=True)
    with col2:
        if st.button("Cerrar", use_container_width=True):
            st.rerun()

def log_error(mensaje, error, contexto=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info_error = f"{timestamp} - {mensaje}: {str(error)}"
    if contexto:
        info_error += f" | Contexto: {contexto}"
    
    logging.error(info_error)
    with open("errores_criticos.txt", "a", encoding="utf-8") as f:
        f.write(info_error + "\n")

# --- ESTADO DE SESIÓN ---
def borrar_todo():
    st.session_state.area_texto_profe = ""
    st.session_state.ultimo_audio_id = None
    st.session_state.descarga_info = None
    logging.info("Sesión reiniciada por el usuario.")

if 'area_texto_profe' not in st.session_state:
    st.session_state.area_texto_profe = ""
if 'ultimo_audio_id' not in st.session_state:
    st.session_state.ultimo_audio_id = None
if 'descarga_info' not in st.session_state:
    st.session_state.descarga_info = None

# Lista de formatos de audio soportados por Gemini
FORMATOS_SOPORTADOS = [
    "audio/wav", "audio/mp3", "audio/aiff", "audio/aac", 
    "audio/ogg", "audio/flac", "audio/webm", "audio/mpeg", "audio/x-wav"
]

st.markdown("""
    <style>
    /* Estética Global y Eliminación de Scroll */
    .stApp { 
        background-color: #0F172A; 
        color: #F8FAFC; 
        font-family: 'Inter', 'Segoe UI', sans-serif;
        overflow: hidden;
    }

    /* Ocultar Menú y Botón de Deploy innecesarios */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Títulos */
    h1 { 
        color: #FACC15 !important; 
        font-size: 50px !important; 
        text-align: center;
        margin-bottom: -20px !important;
    }

    /* Columna de Audio y Texto */
    [data-testid="stVerticalBlock"] > div:has(div[data-testid="stAudioInput"]) {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    /* Botón de Audio GIGANTE y CIRCULAR */
    div[data-testid="stAudioInput"] {
        width: 250px !important;
        transform: scale(1.5);
        border-radius: 100px !important;
    }

    /* Ajuste de Columnas para evitar Scroll */
    .stMainBlockContainer {
        padding-top: 2rem !important;
        max-width: 95% !important;
    }

    /* Cuadros de Texto */
    .stTextArea textarea { 
        font-size: 20px !important; 
        border-radius: 15px !important; 
        background-color: #1E293B !important;
        height: 250px !important;
    }

    /* Botones de Acción */
    .stButton>button { 
        height: 70px !important; 
        font-size: 22px !important; 
        border-radius: 20px !important; 
    }
    
    /* Estilo del Modal */
    div[role="dialog"] {
        background-color: #1E293B !important;
        width: 80% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👩‍🏫 ¡Hola, Profe!")

# Diseño de dos columnas principales
col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.markdown('<p class="big-text">1. Pulse el círculo para hablar:</p>', unsafe_allow_html=True)
    audio_file = st.audio_input("Grabar voz")
    
    if audio_file:
        audio_id = hash(audio_file.getvalue())
        if st.session_state.ultimo_audio_id != audio_id:
            if audio_file.type not in FORMATOS_SOPORTADOS:
                st.error(f"⚠️ Audio no compatible")
                log_error("Formato no soportado", audio_file.type)
            else:
                with st.spinner("Escuchando..."):
                    try:
                        t = transcribir_audio(audio_file.getvalue(), audio_file.type)
                        if "Error" not in t:
                            st.session_state.area_texto_profe = t
                        st.session_state.ultimo_audio_id = audio_id
                        st.rerun()
                    except Exception as e:
                        log_error("Error audio", e)

    st.markdown('<p class="big-text">2. Revise o corrija el texto:</p>', unsafe_allow_html=True)
    st.text_area("", key="area_texto_profe", label_visibility="collapsed")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ ¡HACER TRABAJO!"):
            texto = st.session_state.area_texto_profe
            if texto.strip():
                with st.spinner("Procesando..."):
                    try:
                        res = procesar_peticion_texto(texto)
                        start = res.find('{')
                        end = res.rfind('}') + 1
                        datos_ia = json.loads(res[start:end])
                        
                        accion = datos_ia.get("accion")
                        info = datos_ia.get("datos")
                        
                        if accion == "crear_planeamiento":
                            ruta, nombre = generar_word_planeamiento(info)
                            st.session_state.descarga_info = (ruta, nombre)
                        elif accion == "actualizar_nota":
                            msg = actualizar_nota_excel("data/planilla_notas.xlsx", 
                                                      info.get('alumno'), 
                                                      info.get('materia'), 
                                                      info.get('nota'))
                            st.session_state.mensaje_nota = msg
                            st.balloons()
                    except Exception as e:
                        log_error("Error IA", e)
                        st.error("Hubo un fallo técnico.")
            else:
                st.warning("Hable primero.")
    with c2:
        st.button("🧹 BORRAR", on_click=borrar_todo)

with col_der:
    st.markdown('<p class="big-text">3. Resultado aquí debajo:</p>', unsafe_allow_html=True)
    
    # Mostrar mensaje de nota si existe
    if 'mensaje_nota' in st.session_state and st.session_state.mensaje_nota:
        st.success(st.session_state.mensaje_nota)
        if st.button("Cerrar mensaje"):
            st.session_state.mensaje_nota = None
            st.rerun()

    # Mostrar previsualización y descarga de Word
    if st.session_state.descarga_info:
        ruta, nombre = st.session_state.descarga_info
        if os.path.exists(ruta):
            st.info(f"📄 Plan Listo: {nombre}")
            texto_preview = leer_texto_word(ruta)
            st.text_area("Contenido generado:", texto_preview, height=350)
            
            with open(ruta, "rb") as f:
                st.download_button("📥 GUARDAR EN MI PC", f, file_name=nombre, use_container_width=True)
        else:
            st.error("El archivo se perdió. Intente de nuevo.")
    else:
        st.write("Esperando a que termine el paso 2...")


if os.path.exists("debug_adi.log"):
    with st.sidebar:
        st.header("📚 Biblioteca de Planes")
        st.write("Aquí puede gestionar todos los trabajos que ha realizado.")
        
        archivos = listar_archivos()
        if archivos:
            # Creamos una lista de datos para la tabla
            datos_tabla = []
            for f in archivos:
                ruta = os.path.join("data/output", f)
                fecha = datetime.fromtimestamp(os.path.getmtime(ruta)).strftime("%d/%m/%Y %H:%M")
                datos_tabla.append({"Archivo": f, "Fecha": fecha})
            
            # Buscador simple usando texto
            busqueda = st.text_input("🔍 Buscar plan por nombre:", placeholder="Ej: Matemáticas...")
            
            # Filtrar archivos basado en la búsqueda
            archivos_filtrados = [f for f in archivos if busqueda.lower() in f.lower()]
            
            if archivos_filtrados:
                for f in archivos_filtrados:
                    with st.expander(f"📄 {f[:30]}..."):
                        ruta_f = os.path.join("data/output", f)
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("🔍 VER", key=f"ver_{f}", use_container_width=True):
                                mostrar_plan_modal(ruta_f, f)
                        with c2:
                            if st.button("🗑️ BORRAR", key=f"del_{f}", use_container_width=True):
                                if eliminar_archivo(ruta_f):
                                    st.success("¡Borrado!")
                                    st.rerun()
            else:
                st.warning("No se encontraron planes con ese nombre.")
        else:
            st.info("Aún no tiene planes guardados.")

        st.divider()
        if st.checkbox("⚙️ Configuración Avanzada"):
            st.write("**Herramientas del Sistema**")
            if st.button("🔄 BUSCAR ACTUALIZACIONES", use_container_width=True):
                with st.spinner("Conectando con el servidor..."):
                    msg, reboot = buscar_actualizaciones()
                    if reboot:
                        st.success(msg)
                        st.info("Reiniciando para aplicar cambios...")
                        st.rerun()
                    else:
                        st.info(msg)
            
            st.write("---")
            if st.checkbox("Ver Registro Técnico (Logs)"):
                with open("debug_adi.log", "r") as f:
                    st.text(f.readlines()[-20:])
