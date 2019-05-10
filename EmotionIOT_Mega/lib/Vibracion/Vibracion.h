/**
   \file Vibracion.h
   \brief Funciones de control de Vibracion
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef VIBRACION_H
#define VIBRACION_H

#include <ArduinoSTL.h>

using namespace std;

/**
   \brief Ejecuta un efecto de vibracion
   \param pinVibracion Vector de pines de salida
   \param vibracion Efecto de vibracion
*/
void vibracion(vector<int> pinVibracion, int vibracion){

  switch(vibracion){
    case 1://Tran-Traaan
      for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
        digitalWrite(*motor,HIGH);
      }
      delay(100);
      for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
        digitalWrite(*motor,LOW);
      }
      delay(100);
      for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
        digitalWrite(*motor,HIGH);
      }
      delay(250);
      for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
        digitalWrite(*motor,LOW);
      }
    break;
    case 2://Tran-Tran-Tran
      for(int i=0;i<3;i++){
            if(i!=0){
              delay(100);
              }
              for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
                digitalWrite(*motor,HIGH);
              }
            delay(100);
            for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
              digitalWrite(*motor,LOW);
            }
      }

    break;
    case 3://Traaan
      for(int i=0;i<4;i++){
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,HIGH);
        }
        delay(50);
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,LOW);
        }
      }
    break;
    case 4://Tran
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,HIGH);
        }
        delay(50);
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,LOW);
        }
        delay(20);
    break;
    case 5://Tran,Traan Traaan
      for(int i=1;i<4;i++){
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,HIGH);
        }
        delay(40*i);
        for( auto motor = pinVibracion.begin(); motor != pinVibracion.end(); ++motor ){
          digitalWrite(*motor,LOW);
        }
        delay(40);
      }
    break;
    case 0:
    default:
    break;
  }
}

#endif
