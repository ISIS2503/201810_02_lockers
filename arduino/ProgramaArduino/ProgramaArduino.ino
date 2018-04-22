#include <EEPROM.h>

 

#include <boarddefs.h>

#include <IRremote.h>

#include <IRremoteInt.h>

#include <ir_Lego_PF_BitStreamEncoder.h>

 

 

#define IR_PIN 12

#define SIZE_BUFFER_DATA       50

char        bufferData [SIZE_BUFFER_DATA];

boolean     stringComplete = false;
 

IRrecv ir(IR_PIN);

 

int ledPin = 5;                // choose the pin for the LED

int inputPin = 2;               // choose the input pin (for PIR sensor)

int pirState = LOW;             // we start, assuming no motion detected

int val = 0;

int redPin = 9;

int greenPin = 10;

int bluePin= 11;

int buzzPin=3;

long currTime;

double batteryCharge;

const double MIN_VOLTAGE = 1.2;

const int BATTERY_LED = 7;

 

boolean asterisco = false;

boolean acabe = false;

boolean otroAcabe = false;

boolean encontrado = false;

String  inputString = "";

 

decode_results read;

String lectura[3]={"","",""};

 

int digitosIngresados = 0;

 

int incorrectos = 0;

 

unsigned long startTime;

unsigned long timedos;

unsigned long timeBattery;

boolean flag;

boolean lastValue = false;

 

String color = "AZUL";

String clave = "";

int digitos = 0;

boolean compareKey(String key) {

  int acc = 3;

  int codif, arg0, arg1;

  for(int i=0; i<3; i++) {

    codif = EEPROM.read(i);

    while(codif!=0) {

      if(codif%2==1) {

        arg0 = EEPROM.read(acc);

        arg1 = EEPROM.read(acc+1)*256;

        arg1+= arg0;

        if(String(arg1)==key) {

          return true;

        }

      }

      acc+=2;

      codif>>=1;

    }

    acc=(i+1)*16+3;

  }

  return false;

}

 

//Method that adds a password in the specified index

void addPassword(int val, int index) {

  byte arg0 = val%256;

  byte arg1 = val/256;

  EEPROM.write((index*2)+3,arg0);

  EEPROM.write((index*2)+4,arg1);

  byte i = 1;

  byte location = index/8;

  byte position = index%8;

  i<<=position;

  byte j = EEPROM.read(location);

  j |= i;

  EEPROM.write(location,j);
  Serial.println("added");
}

 

//Method that updates a password in the specified index

void updatePassword(int val, int index) {

  byte arg0 = val%256;

  byte arg1 = val/256;

  EEPROM.write((index*2)+3,arg0);

  EEPROM.write((index*2)+4,arg1);

}

 

//Method that deletes a password in the specified index

void deletePassword(int index) {

  byte i = 1;

  byte location = index/8;

  byte position = index%8;

  i<<=position;

  byte j = EEPROM.read(location);

  j ^= i;

  EEPROM.write(location,j);

}

 

//Method that deletes all passwords

void deleteAllPasswords() {

  //Password reference to inactive

  EEPROM.write(0,0);

  EEPROM.write(1,0);

  EEPROM.write(2,0);

}

 

// Methods that divides the command by parameters

void processCommand(String command) {
  Serial.println("Procesando string");
  Serial.println(command);
  char temp[command.length()];
  command.toCharArray(temp, command.length());
  char* p;
  int i = 0;
  p = strtok(temp,";");
  while(p != NULL){
    lectura[i++] = p;
    p = strtok(NULL,";");
  }

}

 

void receiveData() {

  while (Serial.available()) {
    inputString=Serial.readString();
    Serial.println();
  }

}

 

void buzz()

{

  digitalWrite(buzzPin,HIGH);

  delay(2000);

  digitalWrite(buzzPin,LOW);

}

void checkBattery()

{

  //batteryCharge = (analogRead(3)*5.4)/1024;

  //if(batteryCharge<=-1) {

    //digitalWrite(BATTERY_LED,HIGH);

    //Serial.println("Emergency&&BatteryLow&&3&&cambie La Bateria");

   

    //if(timeBattery>0)

    //{

      //if(((-timeBattery+millis())%30000)<100)

      //{

       

         //buzz();

      //}

    //}

    //else

    //{

      //timeBattery=millis();

      //delay(2000);

      //digitalWrite(buzzPin,LOW);

    //}

 // }

   // else {

    //digitalWrite(BATTERY_LED,LOW);

   // timeBattery=0;

   // digitalWrite(buzzPin,LOW);

  //}

}

void azul(){

  analogWrite(redPin, 0);

  analogWrite(greenPin, 255);

  analogWrite(bluePin, 255);

}

 

void rojo(){

  analogWrite(redPin, 255);

  analogWrite(greenPin, 255);

  analogWrite(bluePin, 0);

}

 

void verde(){

  analogWrite(redPin, 255);

  analogWrite(greenPin, 0);

  analogWrite(bluePin, 255);

}

 

void setup() {

    Serial.begin(9600);

    pinMode(ledPin, OUTPUT);      // declare LED as output

    pinMode(inputPin, INPUT);

    pinMode(redPin, OUTPUT);

    pinMode(greenPin, OUTPUT);

    pinMode(bluePin, OUTPUT);

    pinMode(buzzPin,OUTPUT);

    color = "AZUL";

    azul();

    ir.enableIRIn();

}

 

boolean comprobarAsterisco(){

  if(asterisco){

    return true; 

  }

  else

    return false;

}

 

void check2(){

  val = digitalRead(inputPin);  // read input value

  if (val == HIGH) {            // check if the input is HIGH

    digitalWrite(ledPin, HIGH);  // turn LED ON

    if (pirState == LOW) {

      // we have just turned on

      Serial.println("Emergencia&&Presencia&&1&&inicio");

      // We only want to print on the output change, not state

      pirState = HIGH;

    }

  } else {

    digitalWrite(ledPin, LOW); // turn LED OFF

    if (pirState == HIGH){

      // we have just turned of

      Serial.println("Emergencia&&Presencia&&1&&fin");

      // We only want to print on the output change, not state

      pirState = LOW;

    }

  }

}

 

void check(){  

    if(color.equals("VERDE")){

       if((millis()-currTime)>=30000) {

      Serial.println("Emergencia&&LimiteDeTiempo&&0&&Sin Info");

      rojo();

      color="ROJO";

      buzz();

     

      }

        }

 

      }

 

void loop() {

    check();

    check2();

    checkBattery();

    if(color.equals("ROJO"))

    {

      buzz();

    }

    if (ir.decode(&read)){

        int valor = (read.value);

        if(valor == 26775){

          clave+="1";

          digitos++;

          lastValue = false;

          Serial.println(1);

        }

       

        else if(valor == -26521){

          clave+="2";

          digitos++;

          lastValue = false;

          Serial.println(2);

        }

       

        else if(valor == -20401){

          clave+="3";

          digitos++;

          lastValue = false;

          Serial.println(3);

        }

        else if(valor == 12495){

          clave+="4";

          digitos++;

          lastValue = false;

          Serial.println(4);

        }

       

        else if(valor == 6375){

          clave+="5";

          digitos++;

          lastValue = false;

          Serial.println(5);

        }

       

        else if(valor == 31365){

          clave+="6";

          digitos++;

          lastValue = false;

          Serial.println(6);

        }

       

        else if(valor == 4335){

          clave+="7";

          digitos++;

          lastValue = false;

          Serial.println(7);

        }

       

        else if(valor == 14535){

          clave+="8";

          digitos++;

          lastValue = false;

          Serial.println(8);

        }

       

        else if(valor == 23205){

          clave+="9";

          digitos++;

          lastValue = false;

          Serial.println(9);

        }

        else if(valor == 19125){

          clave+="0";

          digitos++;

          lastValue = false;

          Serial.println(0);

        }

        else if(valor == 21165 && color.equals("ROJO")){

          color="AZUL";

          azul();

          timedos = 0;

          lastValue = false;

        }

        else if(valor == 21165){

          clave="";

          digitos=0;

          lastValue = false;

          Serial.println("#");

        }

        else if(valor == 17085 && color.equals("VERDE")){

          color = "AZUL";

          azul();

          asterisco = true;

          lastValue = false;

          Serial.println("*");

        }

        else if(valor == 19227 || valor ==765 ){

          color = "AZUL";

          azul();

          lastValue = true;

          currTime=millis();

          Serial.println("OK");

        }

        else if(valor == -1 && lastValue){

          color = "VERDE";

          verde();

          lastValue = true;

          Serial.println("Oprimido");

        }

        else if(valor==25245 && color.equals("VERDE")){

          color = "AZUL";

          azul();

          asterisco = true;

          lastValue = false;

          Serial.println("no Oprimido");

        }

        if(digitos==4){

            if(compareKey(clave)){

              color = "VERDE";

              analogWrite(redPin, 255);

              analogWrite(greenPin, 0);

              analogWrite(bluePin, 255);

              acabe = true;

              encontrado = true;

              incorrectos=0;

              currTime=millis();

              }

         

          if (!encontrado){

              rojo();

              color = "ROJO";

              buzz();

              timedos = millis();

              delay(1000);

              azul();

              color = "AZUL";

              incorrectos++;

            }

          if(((incorrectos % 3)==0)&&incorrectos!=0){

              Serial.println("Emergencia&&IntentosExcedidos&&2&&SinInfo");

              rojo();

              color = "ROJO";

              buzz();

              delay(30000);

              azul();

              color = "AZUL";

            }

          clave="";

          acabe = false;

          encontrado = false;

          digitos=0;

          startTime = 0;

        }

        ir.resume();
    }
    receiveData();
    processCommand(inputString);
     if(lectura[0].equals("CHANGE_PASSWORD")){
            int index = lectura[1].toInt();
            int pass = lectura[2].toInt();
            updatePassword(pass,index);
          }
          else if(lectura[0].equals("ADD_PASSWORD")){
            Serial.println("Entre al IFF");
            int index = lectura[1].toInt();
            int pass = lectura[2].toInt();
            addPassword(pass,index);
          }
          else if(lectura[0].equals("DELETE_PASSWORD")){
            Serial.println("Delete password");
            int temp_index = lectura[1].toInt();
            deletePassword(temp_index);
          }
          else if(lectura[0].equals("DELETE_ALL_PASSWORDS"))
          {
            deleteAllPasswords();
          }
}
