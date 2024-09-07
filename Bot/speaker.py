import streamlit as st
from gtts import gTTS
from playsound import playsound
import tempfile
import os
from PIL import Image
from brain import predict_class, get_response, intents

# Configuración de la página
st.set_page_config(
    page_title="UPIIH BOT",  # Título en la ventana del navegador
    page_icon="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif",  # Icono de la página
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
        flex-direction: column; /* Cambia la dirección a columna para que los subtemas estén debajo del título */
        align-items: center;
        padding: 10px;
        background-color: #ffff;
    }
    
    /* Estilos para los logos */
    .header-logo {
        width: 120px; /* Tamaño de imagen aumentado */
        height: 80px; /* Tamaño de imagen aumentado */
        margin: 0 10px; /* Espacio alrededor de las imágenes */
    }
    
    /* Estilos para el texto del encabezado */
    .header-title {
        color: black;
        font-size: 1.5em; /* Tamaño de fuente que se ajusta automáticamente */
        margin: 0; /* Elimina el margen predeterminado */
        text-align: center;
    }
    
    /* Estilos para los subtemas */
    .subtopics {
        text-align: center;
        font-size: 1.5em; /* Tamaño de fuente para pantallas grandes */
        margin: 0; /* Elimina el margen predeterminado */
        color: black;
    }
    
    .subtopics p {
        margin: 0; /* Espacio reducido entre párrafos */
    }

    /* Media queries para hacer el diseño responsivo */
    @media (max-width: 600px) {
        .header-title {
            font-size: 0.9em;
        }
        .subtopics {
            font-size: 1em; /* Tamaño de fuente más pequeño en pantallas más pequeñas */
        }
        .header-logo {
            width: 60px; /* Tamaño de imagen reducido para pantallas pequeñas */
            height: 60px; /* Tamaño de imagen reducido para pantallas pequeñas */
        }
    }
    .circle-img {
        border-radius: 50%;
        width: 100px; /* Ajusta el tamaño según lo necesario */
        height: 100px; /* Ajusta el tamaño según lo necesario */
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

# Sidebar image
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

        # Reproducir audio
        playsound(temp_audio_file_path)
    finally:
        if temp_audio_file:
            try:
                os.unlink(temp_audio_file_path)
            except PermissionError:
                pass  # Manejo de excepción si el archivo aún está en uso

# Inicialización de estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "user.png"  # Ruta del avatar del usuario

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif" if message["role"] == "Bot" else st.session_state.user_avatar):
        st.markdown(message["content"])

# Mensaje inicial
if st.session_state.first_message:
    initial_message = "Hola, ¿cómo puedo ayudarte?"
    with st.chat_message("Bot", avatar="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)  # Hablar el mensaje inicial

# Entrada del usuario
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Implementación del algoritmo de la IA
    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot", avatar="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)  # Hablar la respuesta
