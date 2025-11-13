import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Casa Inteligente - Control por Voz", page_icon="🎙️", layout="centered")

# --- ESTILO VISUAL UNIFICADO ---
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
    margin-top: 1.2em;
    text-align: center;
}
.voice-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.voice-img {
    width: 120px;
    border-radius: 50%;
    padding: 10px;
    background-color: rgba(255,255,255,0.7);
    box-shadow: 0px 2px 8px rgba(0,0,0,0.15);
    margin-bottom: 1em;
}
.bk-root button {
    background: linear-gradient(135deg, #7e57c2, #9575cd);
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75em 1.5em !important;
    font-size: 1em !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}
.bk-root button:hover {
    background: linear-gradient(135deg, #6a1b9a, #7b1fa2) !important;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --- MQTT CONFIG ---
def on_publish(client, userdata, result):
    print("El dato ha sido publicado")

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

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p style="color:#5b3f8c; font-family:Poppins; text-align:center;">Habla con tu casa y controla tus dispositivos fácilmente</p>', unsafe_allow_html=True)

st.markdown('<div class="voice-box">', unsafe_allow_html=True)

# Imagen de micrófono
if os.path.exists("voice_ctrl.jpg"):
    st.image("voice_ctrl.jpg", width=120)
else:
    st.image("https://cdn-icons-png.flaticon.com/512/727/727245.png", width=100)

st.markdown('<p style="color:#4a148c; font-family:Poppins; font-size:1em;">🎤 Toca el botón y habla</p>', unsafe_allow_html=True)

# --- BOTÓN DE ESCUCHA (FUNCIONES ORIGINALES SIN CAMBIOS) ---
stt_button = Button(label="🎧 Iniciar escucha", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=100,
    debounce_time=0,
)

st.markdown('</div>', unsafe_allow_html=True)

# --- ENVÍO MQTT (SIN CAMBIOS FUNCIONALES) ---
if result:
    if "GET_TEXT" in result:
        text = result.get("GET_TEXT")
        st.success(f"🗣️ Comando detectado: **{text}**")

        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": text.strip()})
        ret = client1.publish("mensajeproyecto", message)

        st.info("📡 Enviando comando a los dispositivos...")

    try:
        os.mkdir("temp")
    except:
        pass

st.markdown('</div>', unsafe_allow_html=True)

