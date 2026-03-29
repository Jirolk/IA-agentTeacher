import pandas as pd
from docx import Document
import os

def cargar_planilla_notas(ruta_excel):
    """Lee la lista de alumnos de un Excel."""
    try:
        df = pd.read_excel(ruta_excel)
        return df
    except Exception as e:
        return f"Error al leer Excel: {e}"

def actualizar_nota_excel(ruta_excel, alumno, materia, nota):
    """Simulación de actualización de nota."""
    # Aquí irá la lógica para buscar la celda correcta y escribir
    return f"Se ha registrado {nota} para {alumno} en la materia {materia}."

def generar_word_planeamiento(tema, grado, carpeta_salida="data/output"):
    """Crea un documento Word básico basado en el tema."""
    doc = Document()
    doc.add_heading(f'Plan de Clase: {tema.capitalize()}', 0)
    doc.add_paragraph(f'Grado: {grado}')
    doc.add_paragraph('Objetivos: ...')
    doc.add_paragraph('Contenidos: ...')
    
    archivo_nombre = f"Plan_{tema.replace(' ', '_')}.docx"
    ruta_guardado = os.path.join(carpeta_salida, archivo_nombre)
    doc.save(ruta_guardado)
    return ruta_guardado
