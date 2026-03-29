import streamlit as st
import json
import os
import logging
from datetime import datetime
from ai_logic import transcribir_audio, procesar_peticion_texto
from file_utils import generar_word_planeamiento, actualizar_nota_excel

# Configuración de Logging para DEBUG
logging.basicConfig(
    filename='debug_adi.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.set_page_config(page_title="ADI - Tu Asistente Docente", page_icon="👩‍🏫", layout="wide")

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
    .stApp { background-color: #0E1117; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #F1C40F !important; font-size: 50px !important; text-align: center; }
    .big-text { font-size: 24px !important; color: #BDC3C7; text-align: center; }
    .stTextArea textarea { font-size: 24px !important; border: 3px solid #F1C40F !important; border-radius: 15px !important; }
    .stButton>button { width: 100%; height: 80px !important; font-size: 25px !important; border-radius: 20px !important; }
    div[data-testid="stColumn"]:nth-child(1) button { background-color: #27AE60 !important; color: white !important; }
    div[data-testid="stColumn"]:nth-child(2) button { background-color: #C0392B !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("👩‍🏫 ¡Hola, Profe!")
st.markdown('<p class="big-text">1. Pulse el micrófono para hablar:</p>', unsafe_allow_html=True)

col_mid = st.columns([1, 8, 1])[1]

with col_mid:
    audio_file = st.audio_input("Grabar voz")
    
    if audio_file:
        audio_id = hash(audio_file.getvalue())
        if st.session_state.ultimo_audio_id != audio_id:
            if audio_file.type not in FORMATOS_SOPORTADOS:
                st.error(f"⚠️ El formato de audio {audio_file.type} no es compatible. Intente con otro navegador o grabador.")
                log_error("Formato de audio no soportado", audio_file.type)
            else:
                with st.spinner("Escuchando..."):
                    try:
                        t = transcribir_audio(audio_file.getvalue(), audio_file.type)
                        logging.info(f"Transcripción exitosa ({audio_file.type}): {t[:50]}...")
                        if "Error" not in t:
                            st.session_state.area_texto_profe = t
                        else:
                            st.error(t)
                        st.session_state.ultimo_audio_id = audio_id
                        st.rerun()
                    except Exception as e:
                        log_error("Error en flujo de audio", e)

    st.markdown('<p class="big-text">2. Revise el texto:</p>', unsafe_allow_html=True)
    st.text_area("", height=200, key="area_texto_profe")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ ¡SÍ, HACER EL TRABAJO!"):
            texto = st.session_state.area_texto_profe
            if texto.strip():
                with st.spinner("Procesando con Gemini 2.5..."):
                    try:
                        res = procesar_peticion_texto(texto)
                        logging.debug(f"Respuesta IA raw: {res}")
                        
                        start = res.find('{')
                        end = res.rfind('}') + 1
                        
                        if start == -1 or end == 0:
                            raise ValueError("La respuesta de la IA no contiene un objeto JSON válido.")
                        
                        datos_ia = json.loads(res[start:end])
                        
                        accion = datos_ia.get("accion")
                        info = datos_ia.get("datos")
                        
                        if accion == "crear_planeamiento":
                            ruta, nombre = generar_word_planeamiento(info)
                            st.session_state.descarga_info = (ruta, nombre)
                            st.success(f"Plan generado: {info.get('tema')}")
                            logging.info(f"Archivo generado: {ruta}")
                        
                        elif accion == "actualizar_nota":
                            msg = actualizar_nota_excel("data/planilla_notas.xlsx", 
                                                      info.get('alumno'), 
                                                      info.get('materia'), 
                                                      info.get('nota'))
                            if "✅" in msg:
                                st.success(msg)
                                st.balloons()
                            else:
                                st.warning(msg)
                            logging.info(f"Excel actualizado: {msg}")
                    except json.JSONDecodeError as je:
                        log_error("Error de decodificación JSON", je, contexto=res)
                        st.error("No pude entender la respuesta de la IA. Por favor, intente de nuevo con más detalle.")
                    except Exception as e:
                        log_error("Error procesando petición", e)
                        st.error(f"Hubo un problema técnico: {str(e)}")
            else:
                st.warning("Primero debe hablar o escribir.")

    with c2:
        st.button("🧹 BORRAR TODO", on_click=borrar_todo)

    if st.session_state.descarga_info:
        ruta, nombre = st.session_state.descarga_info
        if os.path.exists(ruta):
            with open(ruta, "rb") as f:
                st.download_button("📥 GUARDAR ARCHIVO", f, file_name=nombre)
        else:
            logging.error(f"El archivo {ruta} no existe para descarga.")

if os.path.exists("debug_adi.log"):
    with st.sidebar:
        st.divider()
        if st.checkbox("Ver Registro Técnico (Logs)"):
            with open("debug_adi.log", "r") as f:
                st.text(f.readlines()[-20:]) # Mostrar últimas 20 líneas
