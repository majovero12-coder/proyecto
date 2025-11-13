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
.stButton>button {
    background: linear-gradient(135deg, #7e57c2, #9575cd);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75em 1.5em;
    font-size: 1em;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    width: 240px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #6a1b9a, #7b1fa2);
    transform: scale(1.05);
}
.subtitle {
    font-family: 'Poppins', sans-serif;
    color: #5b3f8c;
    text-align: center;
    font-size: 1.05em;
    margin-bottom: 1em;
}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN MQTT ---
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
st.markdown('<div class="subtitle">Habla con tu casa y controla tus dispositivos fácilmente</div>', unsafe_allow_html=True)

if os.path.exists("voice_ctrl.jpg"):
    st.image("voice_ctrl.jpg", width=120)
else:
    st.image("https://cdn-icons-png.flaticon.com/512/727/727245.png", width=100)

st.write("🔊 Toca el botón y habla")

# --- BOTÓN DE ESCUCHA (MISMAS FUNCIONES ORIGINALES) ---
stt_button = Button(label="🎧 Iniciar escucha", width=250)

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
    override_height=75,
    debounce_time=0
)

# --- ENVÍO POR MQTT (sin cambios) ---
if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": result.get("GET_TEXT").strip()})
        ret = client1.publish("mensajeproyecto", message)

    try:
        os.mkdir("temp")
    except:
        pass

st.markdown('</div>', unsafe_allow_html=True)
