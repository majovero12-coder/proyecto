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
    /* 🌷 Fondo rosado pastel en degradé horizontal */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(90deg, #ffe5ec 0%, #ffd6e0 50%, #fddde6 100%);
    }

    /* Centrar contenido */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding-top: 10px;
    }

    /* 💕 Título principal */
    h1 {
        text-align: center;
        color: #d63384;
        font-family: 'Quicksand', 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 3em !important;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px rgba(214, 51, 132, 0.2);
        margin-bottom: 0.3em;
    }

    /* 💖 Subtítulo */
    h2, h3 {
        text-align: center;
        color: #a83279;
        font-family: 'Quicksand', 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.6em;
        margin-bottom: 1.5em;
    }

    /* 📸 Imagen rectangular centrada con bordes redondeados */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 20px;
        border: none;
        width: 380px;
        height: auto;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    /* ✨ Texto principal */
    p, div, span {
        font-family: 'Quicksand', 'Poppins', sans-serif;
        color: #4a4a4a;
        text-align: center;
        font-size: 1.05em;
        letter-spacing: 0.3px;
    }

    /* 🌈 Botón */
    .bk-root .bk-btn {
        background: linear-gradient(90deg, #ffb6c1, #f48fb1, #f8a5c2);
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        font-size: 1.3em !important;
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        padding: 12px 40px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        margin-top: 15px;
        width: 240px;
    }

    .bk-root .bk-btn:hover {
        background: linear-gradient(90deg, #f06292, #ec407a, #d81b60);
    }

    /* 💖 Quitar el cuadro blanco inferior */
    div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
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
