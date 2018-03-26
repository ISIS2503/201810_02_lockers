import paho.mqtt.client as mqtt
from pymongo import MongoClient
import datetime
import json
import requests
import sys
import types

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.alertas

def guardar(cadena):
    try:
        #print((((cadena.decode().split(","))[3]).split(":"))[1][1:-2])
        tipo = (((cadena.decode().split(","))[1]).split(":"))[1][1:-1]
        identificador = (((cadena.decode().split(","))[2]).split(":"))[1]
        informacion = (((cadena.decode().split(","))[3]).split(":"))[1][1:-2]
        hora = datetime.datetime.utcnow()
        guardar = {
            'Tipo': tipo,
            'Identificador': identificador,
            'Informacion': informacion,
            'Hora': hora
            }
        collection.insert_one(guardar).inserted_id
    except Exception as e:
        print(e)

def correo(remitente, destinatarios, asunto, cuerpo):
    try:
        data = {
            'cuerpo':cuerpo,
            'asunto': asunto,
            'destinatario': destinatarios,
            'remitente': remitente
            }
        url = 'http://172.24.42.41:8081/mock'
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json=data_json, headers=headers)
    except Exception as e:
        print(e)

def enviar(cadena):
    remitente = 'a@a.com'
    destinatarios = 'b@b.com'
    asunto = 'Alarma'
    cuerpo = cadena
    print(asunto)
    correo(remitente, destinatarios, asunto, cuerpo)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.payload.decode());
    print("Yes!");
    guardar(msg.payload)
    enviar(str(msg.payload))

client = mqtt.Client();
client.on_message=on_message;
client.on_connect=on_connect;
client.connect_async("172.24.42.82",8083,60);
client.reconnect();
client.subscribe("bateria/");
client.subscribe("excedidos/");
client.subscribe("limite/");
client.subscribe("presencia/");
client.subscribe("home/");
client.loop_forever();
