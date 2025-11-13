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
    /* Fondo general con gradiente suave pastel */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffe6f2 0%, #e0d6ff 100%);
    }

    /* Centrado general del contenido */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Título principal */
    h1 {
        text-align: center;
        color: #6c3cb8;
        font-family: 'Comic Sans MS', cursive;
        font-size: 2.8em !important;
        text-shadow: 2px 2px 4px rgba(108, 60, 184, 0.2);
    }

    /* Subtítulo */
    h2, h3 {
        text-align: center;
        color: #7b519d;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
    }

    /* Imagen centrada y con sombra */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Texto */
    p, div, span {
        font-family: 'Poppins', sans-serif;
        color: #333333;
        text-align: center;
    }

    /* Botón del reconocimiento de voz */
    .bk-root .bk-btn {
        background: linear-gradient(135deg, #ffb6c1, #d8b4fe);
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-size: 1.2em !important;
        padding: 10px 25px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    .bk-root .bk-btn:hover {
        background: linear-gradient(135deg, #f472b6, #a78bfa);
        transform: scale(1.08);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }

    /* Ocultar el cuadro blanco debajo del botón */
    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Centrado del botón */
    .bk-root {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

image = Image.open('voice_ctrl.jpg')
st.image(image, width=200)




st.write("Toca el Botón y habla ")

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
