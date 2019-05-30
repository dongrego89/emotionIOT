#include <Macros.h>
#include <Tonos.h>

#include <Interaccion.h>
#include <LectorRFID.h>
#include <EntradaSerial.h>

#include <Arduino.h>

Interaccion interaccionRFID;
int modo;

void setup() {
  vector<int> pinLedAux;
  String opcion;

  //Configuración default interaccionRFID
  pinLedAux.push_back(LEDROJO);
  pinLedAux.push_back(LEDVERDE);

  interaccionRFID.setValores(TONORFID,pinLedAux,EFECTORFID,TIEMPORFID);

  //Inicializar el puerto serie
  Serial.begin(9600);

  //Inicializar el lector RFID
  SPI.begin(); // Iniciar SPI bus
  mfrc522.PCD_Init(); // Iniciar MFRC522

  //Configurar los pines de salida por defecto
  pinMode(LEDAVISO,OUTPUT);

  pinMode(LEDVERDE,OUTPUT);
  pinMode(LEDROJO,OUTPUT);
  
  pinMode(ZUMBADOR,OUTPUT);

  //Inicializar el Modo
  modo=0;
}

void loop(){

  switch(modo){
    case 0:
      modo=entradaSerial();

      if(deteccionTarjeta()){// En caso de leer una tarjeta RFID
        modo=3;
      }
    break;
    case 1:
      digitalWrite(LEDAVISO,HIGH);
      modo=0;
    break;
    case 2:
      digitalWrite(LEDAVISO,LOW);
      modo=0;
    break;
    case 3:
    interaccionRFID.reproducirInteraccion();
    delay(interaccionRFID.getRetardo());
    modo=0;
    break;
    case 4:
      digitalWrite(LEDROJO,HIGH);
      modo=0;
    break;
    case 5:
      digitalWrite(LEDROJO,LOW);
      modo=0;
    break;
    case 6:
      digitalWrite(LEDVERDE,HIGH);
      modo=0;
    break;
    case 7:
      digitalWrite(LEDVERDE,LOW);
      modo=0;
    break;
    default:
      modo=0;
    break;
  }
}
