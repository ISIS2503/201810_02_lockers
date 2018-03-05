import paho.mqtt.client as mqtt

client=mqtt.Client("p1");

def on_message(client, userdata, msg):
    print(msg.payload);
    print("message qos=", msg.qos);
    print("message topic=", msg.topic);

broker_adress="172.24.42.82";
client.connect(broker_adress,port=8083);
client.on_message=on_message;
client.subscribe('home/');
client.subscribe('limite/');
client.subscribe('presencia/');
client.subscribe('excedidos/');
client.publish('home/')
client.loop_forever();
