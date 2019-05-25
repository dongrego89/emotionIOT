/**
   \file main.cpp
   \brief Definición del sketch para Arduino Mega
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#include <Macros.h>
#include <Tonos.h>

#include <Interaccion.h>
#include <Pantalla.h>
#include <Boton.h>
#include <Botonera.h>
#include <LectorRFID.h>
#include <EntradaSerial.h>

int modo;
int botonPulsado;

Interaccion interaccionMQTT, interaccionRFID;
Pantalla pantallaInicio;

Botonera botonera;
Boton nuevoBoton;


void setup() {

  //Modo de inicio para establecer la pantalla de Bienvenida
  modo=1;

  //Arrancar serial a 9600
  Serial.begin(9600);

  vector<int> pinLedAux,pinVibracionAux;
  Pantalla pantallaAuxiliar;
  String opcion;

  //Inicializar la pantalla lcd
  lcd.begin();
  lcd.backlight();

  //Configuración default interaccionRFID
  pinLedAux.push_back(LEDVERDE);
  pinLedAux.push_back(LEDROJO);

  pinVibracionAux.push_back(MOTOR);

  pantallaAuxiliar.setLinea("Tarjeta RFID",4,1);
  interaccionRFID.setValores(TONORFID,pinLedAux,EFECTORFID,pinVibracionAux,0,TIEMPORFID,pantallaAuxiliar);

  //Inicializar el lector RFID
  SPI.begin(); // Iniciar SPI bus
  mfrc522.PCD_Init(); // Iniciar MFRC522

  //Inicializar la pantalla de inicio
  pantallaInicio.setLinea("EmotionIOT", 5, 1);
  pantallaInicio.setLinea("Controller", 5, 2);

  //Inicializar la botonera
  opcion="Opcion ";

  //Introducir 4 botones en botonera
  for(int i=1;i<=4;i++){
    pantallaAuxiliar.vaciar();
    pantallaAuxiliar.setLinea(opcion + i,6,1);

    botonera.setBoton(i,BOTONINICIO+((i-1)*2),5,pinLedAux,2,pinVibracionAux,0,TIEMPOINTERACCION,pantallaAuxiliar);
  }


  //Configurar pines de botones [20-40]
  for(int i=BOTONINICIO;i<=BOTONFIN;i++){
    pinMode(i,INPUT);
  }

  //Configurar pines de botones [41-49]
  for(int i=SALIDAINICIO;i<=SALIDAFIN;i++){
    pinMode(i,OUTPUT);
  }

  //Configurar los pines de salida por defecto
  pinMode(ZUMBADOR,OUTPUT);
  pinMode(MOTOR,OUTPUT);
  pinMode(LEDVERDE,OUTPUT);
  pinMode(LEDROJO,OUTPUT);
}

void loop() {

  switch(modo){
    case 0:
      //Comprobar si se reciben datos por Serial
      modo=entradaSerial(interaccionMQTT,pantallaInicio,nuevoBoton);

      //Comprobar si se reciben bytes por el lector RFID
      if(deteccionTarjeta(interaccionRFID)){
        modo=3;
      }

      //Comprobar si se reciben pulsos de botón
      for(vector<Boton>::iterator it=botonera.getBotones().begin(); it!=botonera.getBotones().end();++it){
        if(digitalRead(it->getPin())==HIGH){
          modo=2;
          botonPulsado=it->getId();
          Serial.print("Boton;"+String(botonPulsado)+";");
        }
      }

    break;
    case 1: //Instruccion de pantalla de inicio
      pantallaInicio.print();
      modo=0;
    break;
    case 2: //Instruccion de interaccion con boton
      botonera.getBoton(botonPulsado).reproducirInteraccion();
      botonera.getBoton(botonPulsado).getPantalla().print();
      delay(botonera.getBoton(botonPulsado).getRetardo());
      botonPulsado=0;
      modo=1;
    break;
    case 3: //Instruccion de interaccion con RFID
      interaccionRFID.reproducirInteraccion();
      interaccionRFID.getPantalla().print();
      delay(interaccionRFID.getRetardo());
      modo=1;
    break;
    case 4: //Instruccion de interaccion con MQTT
      interaccionMQTT.reproducirInteraccion();
      interaccionMQTT.getPantalla().print();

      delay(interaccionMQTT.getRetardo());

      modo=1;
    break;
    case 5: //Instruccion de configuración de boton
      botonera.setBoton(nuevoBoton);
      modo=1;
    break;
    default:
    break;
  }
}
