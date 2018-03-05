#include <boarddefs.h>
#include <IRremote.h>
#include <IRremoteInt.h>
#include <ir_Lego_PF_BitStreamEncoder.h>


#define IR_PIN 12

IRrecv ir(IR_PIN);

int ledPin = 5;                // choose the pin for the LED
int inputPin = 4;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;
int redPin = 9;
int greenPin = 10;
int bluePin= 11;

long currTime;

boolean asterisco = false;
boolean acabe = false;
boolean otroAcabe = false;
boolean encontrado = false;

decode_results read;

String claves[] = {"1234", "2345", "3456", "4567"};

int digitosIngresados = 0;

int incorrectos = 0;

unsigned long startTime;
unsigned long timedos;
boolean flag;
boolean lastValue = false;

String color = "AZUL";

String clave = "";
int digitos = 0;

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
      
      } 
        }

      }

void loop() {
    check();
    check2();
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
          Serial.println("OK"); 
        }
        else if(valor == -1 && lastValue){
          color = "VERDE";
          verde();
          lastValue = true;
          Serial.println("Oprimido");
        }
        if(digitos==4){
          for(int i = 0; i<4 && !acabe; i++){
            if(clave.equals(claves[i])){
              color = "VERDE";
              analogWrite(redPin, 255);
              analogWrite(greenPin, 0);
              analogWrite(bluePin, 255);
              acabe = true;
              encontrado = true;
              incorrectos=0;
              currTime=millis();
              }
          }
          if (!encontrado){
              rojo();
              color = "ROJO";
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
}