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
    margin-bottom: 0.2em;
}
h2 {
    color: #5b3f8c;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 1.3em;
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
.voice-img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 110px;
    border-radius: 50%;
    padding: 10px;
    background-color: rgba(255,255,255,0.7);
    box-shadow: 0px 2px 8px rgba(0,0,0,0.15);
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
