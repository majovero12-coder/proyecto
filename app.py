import streamlit as st
import os
import json
import paho.mqtt.client as paho
import time
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Casa Inteligente - Control por Voz", page_icon="🎙️", layout="centered")

# --- ESTILO VISUAL ---
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
}
h2 {
    color: #5b3f8c;
    text-align: center;
    font-family: 'Poppins', sans-serif;
}
.card {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 2em;
    border-radius: 16px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
    margin-top: 1.2em;
    text-align: center;
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
    background: rgba(255,255,255,0.9);
    border-radius: 10px;
    padding: 1em;
    margin-top: 1em;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    color: #4a148c;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# --- MQTT CONFIG ---
def on_publish(client, userdata, result):
    print("✅ Mensaje publicado correctamente")

broker = "broker.mqttdashboard.com"
port = 1883
client = paho.Client("sofimajo")
client.on_publish = on_publish
client.connect(broker, port)

# --- INTERFAZ ---
st.title("🏠 CASA INTELIGENTE")
st.subheader("🎙️ CONTROL POR VOZ")

st.markdown('<div class="card">', unsafe_allow_html=True)

if os.path.exists("voice_ctrl.jpg"):
    st.image("voice_ctrl.jpg", width=120)
else:
    st.image("https://cdn-icons-png.flaticon.com/512/727/727245.png", width=100)

st.write("🔊 Toca el botón y habla para dar una orden")

# --- BOTÓN Y CAPTURA DE VOZ (HTML + JS) ---
st.markdown("""
<button class="voice-button" id="start-rec">🎧 Iniciar escucha</button>
<div id="result" class="result-box" style="display:none;"></div>

<script>
const button = document.getElementById("start-rec");
const resultBox = document.getElementById("result");

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

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        button.innerText = "🎧 Iniciar escucha";
        button.style.opacity = "1";
        resultBox.innerText = "🗣️ Comando detectado: " + text;
        resultBox.style.display = "block";
        window.parent.postMessage({type: 'speech', text: text}, '*');
    };

    recognition.onerror = () => {
        button.innerText = "🎧 Iniciar escucha";
        button.style.opacity = "1";
    };
} else {
    button.disabled = true;
    button.innerText = "Micrófono no soportado ❌";
}
</script>
""", unsafe_allow_html=True)

# --- ESCUCHA DEL EVENTO DESDE JS ---
speech_input = st.experimental_get_query_params().get("speech", None)

# --- BLOQUE PARA PUBLICAR EN MQTT (simulado) ---
placeholder = st.empty()

# simulamos recepción de evento manual
st.write("💬 Cuando se detecte un comando, se enviará automáticamente a MQTT.")
st.markdown('</div>', unsafe_allow_html=True)

# Aquí iría la lógica real para publicar el texto capturado
# Por ejemplo:
# if speech_input:
#     client.publish("mensajeproyecto", json.dumps({"Act1": speech_input}))
#     placeholder.success(f"📡 Comando enviado: {speech_input}")

