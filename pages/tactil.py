import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

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
values = 0.0
act1="OFF"

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



st.title("MQTT Control")

if st.button('ON'):
    act1="ON"
    client1= paho.Client("sofimajo")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("mensajeproyecto", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('OFF'):
    act1="OFF"
    client1= paho.Client("sofimajo")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("mensajeproyecto", message)
  
    
else:
    st.write('')

values = st.slider('Selecciona el rango de valores',0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("sofimajo")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("mensajeproyecto", message)
    
 
else:
    st.write('')

