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
    /* Fondo con gradiente pastel */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #ffe6f2 0%, #e4d9ff 100%);
    }

    /* Centrar todo el contenido */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: -30px;
    }

    /* Título principal */
    h1 {
        text-align: center;
        color: #673ab7;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.8em !important;
        letter-spacing: 1px;
        text-shadow: 0 2px 6px rgba(0,0,0,0.2);
        margin-bottom: 0.1em;
    }

    /* Subtítulo */
    h2, h3 {
        text-align: center;
        color: #8e24aa;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        margin-bottom: 1.5em;
    }

    /* Imagen centrada y con efecto */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        width: 180px;
        height: 180px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }

    [data-testid="stImage"] img:hover {
        transform: scale(1.08);
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    /* Texto */
    p, div, span {
        font-family: 'Poppins', sans-serif;
        color: #3c3c3c;
        text-align: center;
    }

    /* Botón del reconocimiento de voz */
    .bk-root .bk-btn {
        background: linear-gradient(135deg, #f48fb1, #ce93d8, #9575cd);
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        font-size: 1.2em !important;
        font-family: 'Poppins', sans-serif;
        padding: 12px 35px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    .bk-root .bk-btn:hover {
        background: linear-gradient(135deg, #ec407a, #ab47bc, #7e57c2);
        transform: scale(1.07);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }

    /* Eliminar fondo blanco de contenedores */
    div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Centrado del botón */
    .bk-root {
        display: flex;
        justify-content: center;
    }

    /* Animación sutil en hover general */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .main, h1, h2, [data-testid="stImage"], .bk-root {
        animation: fadeIn 1s ease forwards;
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
