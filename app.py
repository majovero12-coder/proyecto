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
<button class="voice-button" id="speak-btn">🎧 Iniciar escucha</button>
<div id="result" class="result-box" style="display:none;"></div>

<script>
let button = document.getElementById("speak-btn");
let resultDiv = document.getElementById("result");

if ('webkitSpeechRecognition' in window) {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'es-ES';
  recognition.continuous = false;
  recognition.interimResults = false;

  button.onclick = () => {
    recognition.start();
    button.innerText = "🎙️ Escuchando...";
    button.style.opacity = "0.8";
  };

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    button.innerText = "🎧 Iniciar escucha";
    button.style.opacity = "1";
    resultDiv.innerHTML = "🗣️ Comando detectado: <b>" + text + "</b>";
    resultDiv.style.display = "block";
    window.parent.postMessage({type: "speech", value: text}, "*");
  };

  recognition.onerror = function() {
    button.innerText = "🎧 Iniciar escucha";
    button.style.opacity = "1";
  };
} else {
  button.innerText = "Micrófono no soportado ❌";
}
</script>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


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

