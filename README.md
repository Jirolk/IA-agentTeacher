# 👩‍🏫 ADI 2.5 - Asistente Docente Inteligente

**ADI (Asistente Docente Inteligente)** es una herramienta diseñada para simplificar las tareas administrativas y pedagógicas de los docentes mediante el uso de Inteligencia Artificial de última generación (**Gemini 2.5 Flash**).

Este asistente permite transcribir voz en tiempo real para generar planeamientos de clase profesionales y actualizar planillas de notas de forma automatizada, todo desde una interfaz local sencilla y amigable.

---

## 🚀 Funcionalidades Principales

*   **🎙️ Transcripción de Voz:** Habla directamente al asistente y obtén el texto limpio al instante.
*   **📄 Generación de Planeamientos:** Crea documentos Word (.docx) completos con objetivos, secuencia didáctica e indicadores, siguiendo estándares pedagógicos.
*   **📊 Actualización de Notas:** Actualiza automáticamente una planilla Excel (`planilla_notas.xlsx`) con solo decir el nombre del alumno, la materia y la nota.
*   **📚 Biblioteca de Planes:** Guarda, previsualiza (mediante una ventana emergente) y gestiona tus trabajos anteriores sin gastar créditos de IA.
*   **🔄 Auto-Actualización:** Mantén el sistema al día con un solo botón desde la configuración avanzada (vía Git).

---

## 🛠️ Requisitos Previos

Para ejecutar ADI en tu computadora necesitas:

1.  **Python 3.10+**: [Descargar aquí](https://www.python.org/downloads/). *(Asegúrate de marcar "Add Python to PATH" durante la instalación)*.
2.  **Git**: [Descargar aquí](https://git-scm.com/downloads). *(Necesario para las actualizaciones automáticas)*.
3.  **Google Gemini API Key**: Debes tener una clave de API válida guardada en un archivo `.env`.

---

## 📦 Instalación Local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/IA-agentTeacher.git
    cd IA-agentTeacher
    ```

2.  **Configurar el archivo de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto y añade tu API Key:
    ```env
    GOOGLE_API_KEY=tu_clave_aqui
    ```

3.  **Ejecución rápida:**
    Simplemente haz doble clic en el archivo `run_adi.bat`. El sistema creará automáticamente el entorno virtual e instalará las librerías necesarias la primera vez.

4.  **Lanzador Amigable:**
    Para un uso diario sin ventanas negras de consola, utiliza el archivo `Iniciar ADI.vbs`. Puedes crear un acceso directo de este archivo en el escritorio.

---

## 📖 Guía de Uso para la Profe

1.  **Hablar:** Pulsa el icono del micrófono y describe lo que necesitas (ej: *"Ponle un 9 a Juan Pérez en Matemáticas"* o *"Hazme un plan de clase sobre la fotosíntesis para cuarto grado"*).
2.  **Revisar:** El texto aparecerá en el cuadro de edición. Puedes corregir cualquier palabra si es necesario.
3.  **Ejecutar:** Haz clic en **"✅ ¡SÍ, HACER EL TRABAJO!"**.
4.  **Guardar:** 
    *   Si es una nota, verás una confirmación y globos de celebración.
    *   Si es un plan, se abrirá una previsualización. Pulsa **"📥 GUARDAR ARCHIVO"** para descargarlo.

---

## 📂 Estructura del Proyecto

*   `app/`: Código fuente de la aplicación (Lógica IA, Interfaz Streamlit y Utilidades de archivos).
*   `data/`:
    *   `planilla_notas.xlsx`: Base de datos de alumnos (Excel).
    *   `output/`: Carpeta donde se guardan los planes generados.
*   `Iniciar ADI.vbs`: Lanzador invisible para Windows.
*   `run_adi.bat`: Script de arranque y configuración automática.

---

## ⚙️ Mantenimiento y Actualizaciones

Si el desarrollador sube mejoras al repositorio, puedes actualizar ADI fácilmente:
1.  Abre ADI.
2.  Ve a la barra lateral izquierda.
3.  Marca **"⚙️ Configuración Avanzada"**.
4.  Haz clic en **"🔄 BUSCAR ACTUALIZACIONES"**.

---

*Desarrollado con ❤️ para facilitar la labor docente.*
