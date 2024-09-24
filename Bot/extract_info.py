import pdfplumber
import re

# Función para extraer información del PDF
def extraer_info_pdf(pdf_path):
    nombre_asignatura = ""
    unidades = []

    # Abrimos el PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()

            # Buscar el nombre de la asignatura (ajustable según formato)
            if not nombre_asignatura:
                match_asignatura = re.search(r'Asignatura:\s*(.*)', texto)
                if match_asignatura:
                    nombre_asignatura = match_asignatura.group(1).strip()

            # Buscar número de unidad, nombre de unidad y el temario con temas
            # El patrón detecta 'Unidad X', el nombre de la unidad, y subtemas
            unidades += re.findall(r'Unidad\s*(\d+):\s*(.*?)\n(.*?)\n(?=Unidad|\Z)', texto, re.DOTALL)

    return nombre_asignatura, unidades

# Función para extraer subtemas del temario
def extraer_subtemas(temario_texto):
    # El patrón busca temas con formato "n.n Tema" (como 1.1 Tema)
    subtemas = re.findall(r'(\d+\.\d+)\s*(.*)', temario_texto)
    return subtemas

# Función para mostrar los resultados
def mostrar_resultados(nombre_asignatura, unidades):
    print(f"Nombre de la asignatura: {nombre_asignatura}")
    print("\nUnidades encontradas:\n")

    for unidad in unidades:
        numero, nombre_unidad, temario = unidad
        print(f"Unidad {numero}: {nombre_unidad}")
        print("Temario:")

        # Extraer subtemas del temario
        subtemas = extraer_subtemas(temario)
        for subtema in subtemas:
            numero_subtema, descripcion = subtema
            print(f"- {numero_subtema} {descripcion.strip()}")

        print("\n" + "-"*40 + "\n")

# Archivo PDF de ejemplo
pdf_path = "UPIIH-BOT-1\ESIME ISISA S1 FUNDAMENTOS DE ÁLGEBRA.pdf"

# Extraer la información
nombre_asignatura, unidades = extraer_info_pdf(pdf_path)

# Mostrar la información extraída
mostrar_resultados(nombre_asignatura, unidades)
