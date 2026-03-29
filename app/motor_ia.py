import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Instrucciones para el razonamiento superior de Gemini 2.5
SYSTEM_PROMPT = """
Eres ADI 2.5, un asistente pedagógico de última generación.
Tu salida debe ser exclusivamente JSON válido.

Si la orden es un plan de clase:
{
  "accion": "crear_planeamiento",
  "datos": {
    "tema": "Título",
    "grado": "Grado",
    "objetivos": ["..."],
    "inicio": "...",
    "desarrollo": "...",
    "cierre": "...",
    "recursos": ["..."],
    "indicadores": ["..."]
  }
}

Si la orden es una nota:
{
  "accion": "actualizar_nota",
  "datos": {
    "alumno": "Nombre",
    "materia": "Materia",
    "nota": 0
  }
}
"""

def transcribir_audio(audio_bytes, mime_type):
    client = get_client()
    try:
        # Usando el motor 2.5 para una transcripción perfecta
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "Escribe exactamente lo que dice el audio, sin añadir nada:",
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
            ]
        )
        return response.text.strip()
    except Exception as e:
        return f"Error en transcripción: {str(e)}"

def procesar_peticion_texto(texto):
    client = get_client()
    try:
        # Procesamiento avanzado con Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=texto,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type='application/json'
            )
        )
        return response.text
    except Exception as e:
        return f"Error en procesamiento: {str(e)}"
