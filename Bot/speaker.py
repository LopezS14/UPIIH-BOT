import streamlit as st
from gtts import gTTS
import io
import tempfile
from brain import predict_class, get_response, intents

# Configuración de la página
st.set_page_config(
    page_title="UPIIH BOT",
    page_icon="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.markdown("<h1 style='font-size: 20px;'>Genera tu planeacion didactica con ayuda de un chatbot</h1>", unsafe_allow_html=True)

# Header
image_url = 'https://img.freepik.com/foto-gratis/acuarela-color-rojo-oscuro-textura-fondo-pintado-mano-fondo-color-vino-tinto-acuarela_145343-192.jpg?size=626&ext=jpg'
st.markdown("""
    <style>
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        background-color: #ffff;
    }
    
    .header-logo {
        width: 120px;
        height: 80px;
        margin: 0 10px;
    }
    
    .header-title {
        color: black;
        font-size: 1.5em;
        margin:0;
        text-align:center;
    }
    
    .subtopics {
        text-align: center;
        font-size: 1.5em;
        margin: 0;
        color:black;
    }
    
    .subtopics p {
        margin:0;
    }

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
            <h3 class="header-title">Instituto Politecnico Nacional</h3>
            <img src="https://th.bing.com/th/id/R.8119ac7aaccd85c2837ae19087717f56?rik=3mREtV8uaKpCGg&pid=ImgRaw&r=0" class="header-logo">
        </div>
        <div class="subtopics">
            <p>Secretaría Académica</p>
            <p>Dirección de Educación Superior</p>
            <p>Unidad Profesional Interdisciplinaria Campus de Ingenieria Hidalgo</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Fondo de la app
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

# Cargar imagen en el sidebar
user_avatar = "https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/user.png"
st.sidebar.image(user_avatar, use_column_width=True)

# Función para hablar
def speak(text):
    tts = gTTS(text=text, lang='es')
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    st.audio(audio_file, format='audio/mp3')

# Lógica del chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "https://www.example.com/default-avatar.png"  # Cambia a una URL válida

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    initial_message = "Hola, ¿cómo puedo ayudarte?"
    with st.chat_message("Bot"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)

if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)
