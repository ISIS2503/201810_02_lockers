import socket
import sys
import time
from multiprocessing import Process
import paho.mqtt.client as mqtt



client=mqtt.Client("p1")

resta = 0
tiempoLock  = time.time()
healthcheck  = time.time()
tiempoFuera = 0
class tiempo():

    def __init__(self, check, tiempoFuera):
        self.check = check
        self.tiempoFuera =  tiempoFuera

    def changeCheck(check):
        self.check = check

    def changeTiempoFuera(tiempoFuera):
        self.tiempoFuera = tiempoFuera

    def getCheck():
        return self.check

    def getTiempoFuera():
        return self.tiempoFuera

def on_connect(client, userdata, flags, rc):
    client.subscribe("home/")
    print("Connected with result code "+str(rc))

def cambiarCheckTrue():
    global check
    check = True

def cambiarCheckFalse():
    global check
    check = False

def cambiarResta(restaN):
    global resta
    resta = restaN

def cambiarTiempoFuera():
    global tiempoFuera
    tiempoFuera = time.time()
    print("cambiado")

def cambiarTiempoCero():
    global tiempoFuera
    tiempoFuera = 0

def on_message(client, userdata, msg):
    global tiempoFuera
    print(str(tiempoFuera)+' MENSAJE')
    cambiarCheckTrue()
    cambiarTiempoFuera()
    with open('tiempo.txt', 'a') as the_file:
        the_file.write('Hello\n')
    print('HOLA2')
    print(msg.payload)
    print("message qos=", msg.qos)
    print("message topic=", msg.topic)
    print('HOLA3')
    global check
    if(check == False):
        cambiarCheckTrue()
broker_adress="m11.cloudmqtt.com"
client.username_pw_set('kabs', password='kabs')
client.connect(broker_adress,port=14337)
    
def enviar(objet):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    while True:
        try:
            while True:
                # Send data
                time.sleep(5)
                print("toSend")
                message='heartBeat'
                sock.sendall(message.encode())
                print("sent")
                time.sleep(5)
                # Look for the response  
        except e:
            print(e)
            #sock.connect(server_address)
                
def mqttserver(objet):
    client.on_connect=on_connect
    print('HOLA4')
    print(str(objet.tiempoFuera)+str('JUEPUTA'))
    client.on_message=on_message
    print('HOLA QLIAN')
    print(client)
    print('HOLA5')
    print(client)
    client.loop_forever()

def mirarHora(objet):
    tiempoI = time.time()
    while True:
        print(str(objeto.tiempoFuera)+' LOOP')
        if(objeto.check):
            objeto.tiempoFuera = time.time()
            print(str(objeto.tiempoFuera)+' FUERA CHECK')
            time.sleep(2)
        print(str(objeto.tiempoFuera)+'  2')
        time.sleep(2)
        print(str(tiempoI)+' Tiempo I')
        print('Diferencia: '+str(objeto.tiempoFuera-tiempoI))
        if((objeto.tiempoFuera-tiempoI>10)):
            print('Fuera de linea')
            time.sleep(5)
            tiempoI = time.time()
            cambiarCheckFalse()

objeto = tiempo(True, 0)
print(objeto.check)
if __name__ == '__main__':
  p1 = Process(target=enviar, args=(objeto,))
  p1.start()
  p2 = Process(target=mqttserver, args=(objeto,))
  p2.start()
  p3 = Process(target=mirarHora, args=(objeto,))
  p3.start()
  
  
