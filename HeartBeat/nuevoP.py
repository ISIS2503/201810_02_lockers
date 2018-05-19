import paho.mqtt.client as mqtt
from pymongo import MongoClient
import datetime
import json
import requests
import sys
import types



def guardar(cadena):
    try:
        print(cadena)
        print(cadena.decode())
        j=json.loads(cadena.decode())
        requests.post("http://172.24.42.82:8083/alarmas",data=j)
    except Exception as e:
        print(e)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print("Yes!");
    guardar(msg.payload)

client = mqtt.Client();
client.on_message=on_message;
client.on_connect=on_connect;
client.username_pw_set('kabs', password='kabs')
client.connect_async("m11.cloudmqtt.com",14337,60);
client.reconnect();
client.subscribe("bateria/");
client.subscribe("excedidos/");
client.subscribe("limite/");
client.subscribe("presencia/");
client.loop_forever();
