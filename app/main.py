import streamlit as st
from ai_logic import procesar_peticion

st.set_page_config(page_title="ADI - Asistente Docente", page_icon="👩‍🏫")

# Estilo para que sea fácil de leer (Senior-Friendly)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        height: 3em;
        width: 100%;
        font-size: 1.2em;
        border-radius: 10px;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Hola Profesora 👋")
st.write("Escriba o hable lo que necesita hacer hoy:")

# Entrada de texto simple
user_input = st.text_input("Ejemplo: 'Hoy María sacó un 10' o 'Quiero un plan de clase sobre fotosíntesis'", key="input")

if st.button("Ayúdame con esto"):
    if user_input:
        with st.spinner("Procesando..."):
            resultado = procesar_peticion(user_input)
            # Por ahora solo mostramos lo que la IA interpreta (el JSON)
            # En el siguiente paso, esto disparará la edición del archivo real.
            st.subheader("Entendido. Esto es lo que haré:")
            st.code(resultado)
            st.success("Listo. En el próximo paso conectaré esto con tus archivos de Excel y Word.")
    else:
        st.warning("Por favor, escriba algo para empezar.")

st.sidebar.title("Instrucciones")
st.sidebar.info("Este asistente le ayuda a no tener que pelear con Excel y Word. Solo dígame qué necesita y yo lo haré por usted.")
