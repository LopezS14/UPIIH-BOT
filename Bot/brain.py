import random
import io
import streamlit as st
import json
import pickle
import numpy as np
import requests
from datetime import datetime
from docx import Document as DocxDocument
from tensorflow.keras.models import load_model
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer

# Descargar recursos necesarios de NLTK si no están ya disponibles
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Función para descargar archivos desde URLs
def download_file(url, local_filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error al descargar el archivo desde {url}: {e}")

# URLs de los archivos
intents_url = 'https://raw.githubusercontent.com/LopezS14/UPIIH-BOT/main/Bot/intents.json'
words_url = 'https://raw.githubusercontent.com/LopezS14/UPIIH-BOT/main/Bot/words.pkl'
classes_url = 'https://raw.githubusercontent.com/LopezS14/UPIIH-BOT/main/Bot/classes.pkl'
model_url = 'https://github.com/LopezS14/UPIIH-BOT/raw/main/Bot/chatbot_model.h5'

# Descargar archivos
download_file(intents_url, 'intents.json')
download_file(words_url, 'words.pkl')
download_file(classes_url, 'classes.pkl')
download_file(model_url, 'chatbot_model.h5')

# Cargar archivos locales
try:
    with open('intents.json') as f:
        intents = json.load(f)
    with open('words.pkl', 'rb') as f:
        words = pickle.load(f)
    with open('classes.pkl', 'rb') as f:
        classes = pickle.load(f)
    model = load_model('chatbot_model.h5')
except Exception as e:
    print(f"Error al cargar los archivos: {e}")

# Pasar las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convertir la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecir la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.argmax(res)
    category = classes[max_index]
    return category

# Diccionario de rutas de documentos
doc_paths = {
    "Sistemas automotrices semestre 7": "automotricesSemestre7.docx",
    "Ingenieria mecatronica semestre 1": "mecatronica1.docx",
    "Sistemas automotrices semestre 7-programasintetico": "SA_PS7.pdf",
    "Ingenieria mecatronica semestre 1-programasintetico": "M_PS1.pdf"
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
            
            # Mostrar botón de descarga en la interfaz de Streamlit
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
