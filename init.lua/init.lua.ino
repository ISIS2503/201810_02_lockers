#include <PubSubClient.h>
#include <ESP8266WiFi.h>

//DEFINES
#define TOPIC_SUBSCRIBE        "presencia/"
#define TOPIC_SUBSCRIBE2        "excedidos/"
#define TOPIC_SUBSCRIBE3       "limte/"
#define TOPIC_SUBSCRIBE4       "claves/"
#define TOPIC_PUBLISH          "home/"
#define SIZE_BUFFER_DATA       50

long timeNow;

//VARIABLES
const char* idDevice = "cerradura";
boolean     stringComplete = false;
boolean     init_flag = false;
String      inputString = "";
char        bufferData [SIZE_BUFFER_DATA];

// CLIENTE WIFI & MQTT
WiFiClient    clientWIFI;
PubSubClient  clientMQTT(clientWIFI);

// CONFIG WIFI
const char* ssid = "kiubo";
const char* password = "quemas98";

// CONFIG MQTT
IPAddress serverMQTT (172,24,42,82);
const char* mqtt_server="m11.cloudmqtt.com";
const uint16_t portMQTT = 14337;
const char* usernameMQTT = "kabs";
const char* passwordMQTT = "kabs";

void connectWIFI() {
  // Conectar a la red WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void reconnectWIFI() {
  // Conectar a la red WiFi
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.write(payload, length);
  Serial.println();
}

void setup() {
  Serial.begin(9600);
  inputString.reserve(100);

  clientMQTT.setServer(mqtt_server, portMQTT);
  clientMQTT.setCallback(callback);
  connectWIFI();
  delay(1000);
}

void processData() {
  if (WiFi.status() == WL_CONNECTED) {
    if(init_flag == false) {
      init_flag = true;

      boolean conectMQTT = false;
      if (!clientMQTT.connected()) {
        if (!clientMQTT.connect(idDevice, usernameMQTT, passwordMQTT)) {
        //if (!clientMQTT.connect(idDevice)) {
          conectMQTT = false;
        }
        conectMQTT = true;
      }
      else {
        conectMQTT = true;
      }
      if(conectMQTT) {
        if(clientMQTT.subscribe(TOPIC_SUBSCRIBE)) {
           Serial.println("Subscribe OK");
        }
        if(clientMQTT.subscribe(TOPIC_SUBSCRIBE2)) {
           Serial.println("Subscribe2 OK");
        }
        if(clientMQTT.subscribe(TOPIC_SUBSCRIBE3)) {
           Serial.println("Subscribe3 OK");
        }
        if(clientMQTT.subscribe(TOPIC_SUBSCRIBE4)){
          Serial.println("Subscribe4 OK");
        }
      }
    }

    if (stringComplete && clientMQTT.connected()) {
      if(clientMQTT.publish(TOPIC_PUBLISH, bufferData)) {
        Serial.println(inputString);
        inputString = "";
        stringComplete = false;
      }
      init_flag = false;
    }
  }
  else {
    connectWIFI();
    init_flag = false;
  }
  clientMQTT.loop();
}

void receiveData() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
    }
  }
}
boolean heartBeat=false;
void loop() {
  receiveData();
  processData();
  if(!heartBeat)
  {
   timeNow=millis(); 
   heartBeat=true;
  }
  if(millis()-timeNow>10000){
    heartBeat=false;
    Serial.println("enviando");
    clientMQTT.publish(TOPIC_PUBLISH,"HeartBeat&&HeartBeat&&4&&HeartBeat");
  }
}
