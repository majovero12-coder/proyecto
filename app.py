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
    /* 🌈 Fondo con gradiente pastel */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffe6f9 0%, #e0d6ff 100%);
        animation: fadeIn 1.2s ease-in;
    }

    /* ✨ Centrar contenido */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding-top: 10px;
    }

    /* 🌸 Título principal */
    h1 {
        text-align: center;
        color: #a63ec5;
        font-family: 'Baloo 2', 'Comic Sans MS', cursive;
        font-weight: 800;
        font-size: 2.9em !important;
        letter-spacing: 1px;
        text-shadow: 0 3px 6px rgba(166, 62, 197, 0.3);
        margin-bottom: 0.2em;
    }

    /* 💜 Subtítulo */
    h2, h3 {
        text-align: center;
        color: #9b4edd;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1.2em;
    }

    /* 💫 Imagen redonda con brillo */
    [data-testid="stImage"] img {
        display: block;
        margin: auto;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        box-shadow: 0 0 25px rgba(170, 85, 255, 0.3);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        border: 4px solid white;
    }

    [data-testid="stImage"] img:hover {
        transform: scale(1.1);
        box-shadow: 0 0 35px rgba(240, 100, 255, 0.6);
    }

    /* 🎀 Texto normal */
    p, div, span {
        font-family: 'Poppins', sans-serif;
        color: #4a4a4a;
        text-align: center;
        font-size: 1.05em;
    }

    /* 🎤 Botón de voz */
    .bk-root .bk-btn {
        background: linear-gradient(135deg, #ff80ab, #ce93d8, #b39ddb);
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        font-size: 1.2em !important;
        font-family: 'Baloo 2', 'Poppins', sans-serif;
        font-weight: 600;
        padding: 12px 40px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        margin-top: 15px;
        width: 220px;
    }

    .bk-root .bk-btn:hover {
        background: linear-gradient(135deg, #f06292, #ba68c8, #9575cd);
        transform: scale(1.08);
        box-shadow: 0 8px 22px rgba(0,0,0,0.3);
    }

    /* 💖 Eliminar fondo blanco que aparece debajo del botón */
    div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* 🪩 Centrado del botón */
    .bk-root {
        display: flex;
        justify-content: center;
    }

    /* 🌟 Animación de aparición */
    @keyframes fadeIn {
        from {opacity: 0; transform: translate



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
