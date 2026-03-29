import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: No se encontró GOOGLE_API_KEY en el archivo .env")
else:
    genai.configure(api_key=api_key)
    print("--- Modelos disponibles para tu API Key ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"ID: {m.name} | Descripción: {m.description}")
    except Exception as e:
        print(f"Error al listar modelos: {e}")
