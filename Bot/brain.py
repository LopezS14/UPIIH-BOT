import random
import io
import streamlit as st
import json
import pickle
import numpy as np
from datetime import datetime
from docx import Document as DocxDocument
from tensorflow.keras.models import load_model
#from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Importamos los archivos generados en el código anterior
intents = json.loads(open('https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/intents.json').read())
words = pickle.load(open('https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/words.pkl', 'rb'))
classes = pickle.load(open('https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/classes.pkl, 'rb'))
model = load_model('https://github.com/LopezS14/UPIIH-BOT/edit/main/Bot/brain.py')

# Pasamos las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecimos la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Diccionario de rutas de documentos
doc_paths = {
    "Sistemas automotrices semestre 7": "C:/Users/Deyanira LS/Desktop/Bot/automotricesSemestre7.docx",
    "Ingenieria mecatronica semestre 1 ": "C:/Users/Deyanira LS/Desktop/Bot/mecatronica1.doc",
    "Sistemas automotrices semestre 7-programasintetico":"https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/SA_PS7.pdf",
    "Ingenieria mecatronica semestre 1-programasintetico":"https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M_PS1.pdf"
    
}

# Función para manejar el documento y proporcionar el botón de descarga
def handle_document(tag):
    result = ""
    doc_path = doc_paths.get(tag)
    
    if not doc_path:
        return "Documento no encontrado para el semestre o carrera solicitado."

    # Determinar si el archivo es un .docx o un .pdf
    if doc_path.endswith('.docx'):
        try:
            doc = DocxDocument(doc_path)
            # Acceder a la tabla específica
            if len(doc.tables) > 0:
                tabla_fecha = doc.tables[0]  # Acceder a la primera tabla
                if len(tabla_fecha.rows) > 0 and len(tabla_fecha.columns) > 1:
                    fila_index = 0
                    columna_index = 1
                    # Accede a la celda específica 
                    celda = tabla_fecha.rows[fila_index].cells[columna_index]
                    current_date = datetime.today().strftime('%m/%d/%y %H:%M:%S')
                    celda.text = f"Fecha: {current_date}"
            
            # Guardar en un buffer en memoria
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Mostrar botón de descarga en la interfaz de streamlit
            st.download_button(
                label="Descargar Temario",
                data=buffer,
                file_name=f"Temario_{tag.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        except Exception as e:
            result = f"Ocurrió un error al manejar el archivo DOCX: {e}"
    
    elif doc_path.endswith('.pdf'):
        try:
            # Leer el archivo PDF en un buffer
            with open(doc_path, "rb") as pdf_file:
                pdf_buffer = pdf_file.read()
            
            # Mostrar botón de descarga para el PDF
            st.download_button(
                label="Descargar programa sintetico",
                data=pdf_buffer,
                file_name=f"Programa_Sintetico_{tag.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        
        except Exception as e:
            result = f"Ocurrió un error al manejar el archivo PDF: {e}"
    
    return result

# Obtener una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])   
            break

    # Manejar los documentos para diferentes semestres
    if tag in doc_paths:
        result += handle_document(tag)
    
    return result
