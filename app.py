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



st.title("CASA INTELIGENTE")
st.subheader("CONTROL POR VOZ")

st.markdown("""
    <style>
    /* 🌸 Fondo rosado claro completo */
    [data-testid="stAppViewContainer"] {
        background-color: #ffe6f2;
    }

    /* Contenedor central */
    div.block-container {
        background: transparent !important;
        padding-top: 40px !important;
        margin: 0 auto !important;
        max-width: 900px !important;
    }

    /* 💕 Título principal */
    h1 {
        text-align: center;
        color: #b33c7d;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 2.8em !important;
        letter-spacing: 0.5px;
        margin-bottom: 0.2em;
    }

    /* 💖 Subtítulo */
    h2, h3 {
        text-align: center;
        color: #a23a73;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 1.5em;
        margin-bottom: 1.8em;
    }

    /* 📸 Imagen centrada */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-bottom: 25px !important;
    }

    [data-testid="stImage"] img {
        display: block;
        margin: auto;
        border-radius: 15px;
        width: 350px;
        height: auto;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: none;
    }

    /* 🌷 Botón centrado y elegante */
    .bk-root .bk-btn {
        background: linear-gradient(90deg, #f7b6cc, #f28bb2);
        color: white !important;
        border-radius: 40px !important;
        border: none !important;
        font-size: 1.2em !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        padding: 12px 40px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        width: 220px;
        margin: 20px auto 0 auto;
        display: block;
    }

    .bk-root .bk-btn:hover {
        background: linear-gradient(90deg, #f06b98, #d64a7c);
    }

    /* 💖 Eliminar cualquier recuadro blanco */
    div[data-testid="stVerticalBlock"],
    div[data-testid="stVerticalBlock"] > div,
    .stElementContainer {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 auto !important;
    }

    /* Centrar el botón */
    .bk-root {
        display: flex;
        justify-content: center !important;
    }

    /* Sidebar limpia */
    [data-testid="stSidebar"] {
        background-color: #fafafa !important;
        border-right: none !important;
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
