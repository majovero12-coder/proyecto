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
    /* Fondo animado tipo gradiente en movimiento */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a1c4fd, #c2e9fb);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Títulos grandes y con sombra */
    h1, h2 {
        color: #6a00f4;
        text-shadow: 2px 2px 8px rgba(160, 80, 255, 0.5);
        text-align: center;
    }

    /* Botón con animación pulsante */
    button {
        background: linear-gradient(90deg, #ff6f91, #ff9671);
        color: white !important;
        border-radius: 16px;
        font-size: 18px;
        font-weight: 700;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.5);
    }

    /* Imagen centrada con borde redondeado y sombra */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    [data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }

    /* Texto instructivo centrado y más grande */
    p, label, span, h3 {
        font-size: 18px;
        color: #2d2d2d;
        text-align: center;
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
