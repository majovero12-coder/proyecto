import os
import streamlit as st
import paho.mqtt.client as paho
import json
import time
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Casa Inteligente - Control por Voz", page_icon="🎙️", layout="centered")

# --- ESTILO VISUAL (idéntico al panel táctil) ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ede7f6 0%, #f3e5f5 100%);
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(8px);
}
h1 {
    color: #3a2c5a;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    margin-bottom: 0.3em;
}
h2 {
    color: #5b3f8c;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 1em;
}
.card {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 2em;
    border-radius: 16px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
    margin-top: 2em;
    text-align: center;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}
.voice-button {
    background: linear-gradient(135deg, #7e57c2, #9575cd);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.9em 2em;
    font-size: 1em;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: all 0.3s ease;
}
.voice-button:hover {
    background: linear-gradient(135deg, #6a1b9a, #7b1fa2);
    transform: scale(1.05);
}
.result-box {
    background-color: rgba(255,255,255,0.9);
    border-radius: 10px;
    padding: 1em;
    margin-top: 1em;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    color: #4a148c;
    font-weight: 500;
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES MQTT ---
def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("sofimajo")
client1.on_message = on_message

# --- INTERFAZ PRINCIPAL ---
st.title("🏠 CASA INTELIGENTE")
st.subheader("🎙️ CONTROL POR VOZ")

# ---- TARJETA PRINCIPAL ----
st.markdown('<div class="card">', unsafe_allow_html=True)

# Imagen central
if os.path.exists('voice_ctrl.jpg'):
    image = Image.open('voice_ctrl.jpg')
    st.image(image, width=150)
else:
    st.image("https://cdn-icons-png.flaticon.com/512/727/727245.png", width=100)

st.markdown('<p style="color:#4a148c;font-family:Poppins;">🎤 Toca el botón y habla</p>', unsafe_allow_html=True)

# --- BOTÓN DE ESCUCHA (con JavaScript real y mismo estilo) ---
st.markdown("""
<button class="voice-button" id="speak-btn">🎧 Iniciar escucha</button>
<div id="result" class="result-box" style="display:none;"></div>

<script>
let button = document.getElementById("speak-btn");
let resultDiv = document.getElementById("result");

if ('webkitSpeechRecognition' in window) {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'es-ES';
  recognition.continuous = false;
  recognition.interimResults = false;

  button.onclick = () => {
    recognition.start();
    button.innerText = "🎙️ Escuchando...";
    button.style.opacity = "0.8";
  };

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    button.innerText = "🎧 Iniciar escucha";
    button.style.opacity = "1";
    resultDiv.innerHTML = "🗣️ Comando detectado: <b>" + text + "</b>";
    resultDiv.style.display = "block";
    window.parent.postMessage({type: "speech", value: text}, "*");
  };

  recognition.onerror = function() {
    button.innerText = "🎧 Iniciar escucha";
    button.style.opacity = "1";
  };
} else {
  button.innerText = "Micrófono no soportado ❌";
}
</script>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
