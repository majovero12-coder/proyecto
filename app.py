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
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e8eaf6 0%, #f3e5f5 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.4);
        backdrop-filter: blur(10px);
    }

    [data-testid="stSidebar"] {
        background-color: #ede7f6;
    }

    h1 {
        color: #4a148c;
        font-family: 'Poppins', sans-serif;
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
        box-shadow: 0px 3px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5e35b1, #7b1fa2);
        transform: scale(1.05);
    }

    .card {
        background-color: rgba(255,255,255,0.8);
        border-radius: 16px;
        padding: 1.5em;
        margin-top: 1.2em;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    .slider-label {
        color: #6a1b9a;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        margin-bottom: 0.5em;
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

