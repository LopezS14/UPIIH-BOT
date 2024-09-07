import streamlit as st
from gtts import gTTS
import pygame
import os
import tempfile
from brain import predict_class, get_response, intents
st.markdown ("""
<nav class="navbar bg-body-tertiary">
  <div class="container-fluid">
    <h2>I N S T I T O P O L I T E C N I C O N A C I O N A L</h2>
    <h3>SECRETARIA ACADEMICA</h3>
    <h3>DIRECCION DE EDUCACION SUPERIOR</h3>
  </div>
           
</nav>
<style>

    h2{
      align:center;
      color: white; }
    
</style>
""", 
unsafe_allow_html=True
)
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
user_avatar = "https://github.com/LopezS14/UPIIH-BOT/tree/main/Bot"  # Asegúrate de que la ruta es correcta

# Asegúrate de que la imagen existe

#logica de motracion de la interfaz

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "user.png"  # Ruta del avatar del usuario

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="https://github.com/LopezS14/UPIIH-BOT/blob/main/Bot/M3.gif" if message["role"] == "Bot" else st.session_state.user_avatar):
        st.markdown(message["content"])

if st.session_state.first_message:
    initial_message = "Hola, ¿cómo puedo ayudarte?"
    with st.chat_message("Bot", avatar="M3.gif"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)  # Hablar el mensaje inicial

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
