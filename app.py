import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("sofimajo")
client1.on_message = on_message



st.title("INTERFACES MULTIMODALES")
st.subheader("CONTROL POR VOZ")

st.markdown("""
<style>
/* Fondo morado hermoso */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d9c8ff 0%, #f3e5ff 100%);
}

/* Títulos */
h1, h2 {
    text-align: center;
    color: #3a2c5a;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
}

/* Centrar la imagen */
.img-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Imagen redondeada y sombra suave */
.voice-img {
    width: 130px;
    margin-top: 10px;
    margin-bottom: 10px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.20);
}

/* ---- ESTILO ESPECIAL DEL BOTÓN BOKEH ---- */
.bk-root .bk-btn {
    background: linear-gradient(135deg, #7e57c2, #9575cd) !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 10px 20px !important;
    font-size: 15px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2) !important;
    transition: 0.25s ease-in-out !important;
    cursor: pointer !important;
}

.bk-root .bk-btn:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #6a1b9a, #7b1fa2) !important;
}
</style>
""", unsafe_allow_html=True)


image = Image.open('voice_ctrl.jpg')
st.image(image, width=350)  # Imagen centrada y más grande

# Texto instructivo visible y centrado
st.markdown("<h3 style='text-align:center; color:#ff4d6d;'>Pulsa el botón y habla para enviar tu comando 🚀</h3>", unsafe_allow_html=True)

stt_status = st.empty()  # Esto crea un lugar vacío para actualizar el estado
stt_status.markdown("🎤 Esperando tu comando...")
stt_button = Button(label=" Inicio ", width=200)

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
        if ( value != "") {
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
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("mensajeproyecto", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
