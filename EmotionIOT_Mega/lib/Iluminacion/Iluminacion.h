/**
  \file Iluminacion.h
  \brief Funciones de control de iluminacion
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef ILUMINACION_H
#define ILUMINACION_H

#include <ArduinoSTL.h>

using namespace std;

/**
   \brief Ejecuta un efecto de ilumnación
   \param pinLed Vector de pines de salida
   \param iluminacion Efecto de iluminacion
*/
void iluminacion(vector<int> pinLed, int iluminacion){

  switch(iluminacion){
    case 1:
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,HIGH);
      }
      delay(100);
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,LOW);
      }
      delay(100);
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,HIGH);
      }
      delay(250);
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,LOW);
      }
    break;
    case 2:
      for(int i=0;i<3;i++){
            if(i!=0){
              delay(100);
              }
              for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
                digitalWrite(*led,HIGH);
              }
            delay(100);
            for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
              digitalWrite(*led,LOW);
            }
      }

    break;
    case 3:
    for(int i=0; i<3; i++){
      if(i!=0){
        delay(50);
      }
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,HIGH);
      }
      delay(50);
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,LOW);
      }
    }

    break;
    case 4:
    for(int i=0; i<3; i++){
      if(i!=0){
        delay(30);
      }
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,HIGH);
      }
      delay(30);
      for( auto led = pinLed.begin(); led != pinLed.end(); ++led ){
        digitalWrite(*led,LOW);
      }
    }
    break;
    case 0:
    default:
    break;
  }
}

#endif
