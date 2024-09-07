import streamlit as st
from gtts import gTTS
import pygame
from PIL import Image
import os
import tempfile
from brain import predict_class, get_response, intents

st.set_page_config(
    page_title="UPIIH BOT",  # El título que aparecerá en la ventana del navegador
    page_icon="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif",  # Puedes usar un emoji o la ruta a un archivo de icono
    layout="wide",  # Opcional: "wide" o "centered"
    initial_sidebar_state="expanded"  # Opcional: "expanded" o "collapsed"
)

# Sidebar
st.sidebar.markdown("<h1 style='font-size: 20px;'>Genera tu planeación didáctica con ayuda de un chatbot</h1>", unsafe_allow_html=True)

# Header
image_path = "https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif"
image = Image.open(image_path)
image_url = 'https://img.freepik.com/foto-gratis/acuarela-color-rojo-oscuro-textura-fondo-pintado-mano-fondo-color-vino-tinto-acuarela_145343-192.jpg?size=626&ext=jpg'

st.markdown("""
    <style>
    /* Estilos para el contenedor del encabezado */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        background-color: #ffff;
    }
    
    /* Estilos para los logos */
    .header-logo {
        width: 120px;
        height: 80px;
        margin: 0 10px;
    }
    
    /* Estilos para el texto del encabezado */
    .header-title {
        color: black;
        font-size: 1.5em;
        margin:0;
        text-align:center;
    }
    
    /* Estilos para los subtemas */
    .subtopics {
        text-align: center;
        font-size: 1.5em;
        margin: 0;
        color:black;
    }
    
    .subtopics p {
        margin:0;
    }

    /* Media queries para hacer el diseño responsivo */
    @media (max-width: 600px) {
        .header-title {
            font-size: 0.9em;
        }
        .subtopics {
            font-size: 1em;
        }
        .header-logo {
            width:60px;
            height: 60px;
        }
    }
    .circle-img {
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; width: 100%; align-items: center;">
            <img src="https://th.bing.com/th/id/OIP.MQI9waMb4IGJ52U8KF5gmgHaHa?rs=1&pid=ImgDetMain" class="header-logo">
            <h3 class="header-title">Instituto Politécnico Nacional</h3>
            <img src="https://th.bing.com/th/id/R.8119ac7aaccd85c2837ae19087717f56?rik=3mREtV8uaKpCGg&pid=ImgRaw&r=0" class="header-logo">
        </div>
        <div class="subtopics">
            <p>Secretaría Académica</p>
            <p>Dirección de Educación Superior</p>
            <p>Unidad Profesional Interdisciplinaria Campus de Ingeniería Hidalgo</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image(image, use_column_width=True)

def speak(text):
    temp_audio_file = None
    try:
        # Crear archivo temporal
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='es')
        tts.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name
        temp_audio_file.close()

        # Inicializar pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file_path)
        pygame.mixer.music.play()

        # Esperar a que termine de reproducir
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if temp_audio_file:
            try:
                os.unlink(temp_audio_file_path)
            except PermissionError:
                pass  # Manejo de excepción si el archivo aún está en uso

# Ruta de la imagen
user_avatar = "https://github.com/LopezS14/UPIIH-BOT/blob/
