/**
   \file EntradaSerial.h
   \brief Definición de funciones procesamiento de mensajes Serial
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef ENTRADASERIAL_H
#define ENTRADASERIAL_H

#include <ArduinoSTL.h>

/**
   \brief Procesa la linea de entrada serial y la transforma en el objeto correspondiente
   \return Número con el código del elemento que ha sido procesado
*/

int entradaSerial(){
  char token1=';';

  int retorno=0;

  String data1, campo0;


  if (Serial.available()){
    data1 = Serial.readStringUntil('\n');
    data1.trim();

    //Procesamiento del tipo de mensaje
    campo0=data1.substring(0,data1.indexOf(token1));
    data1=data1.substring(campo0.length()+1);

    retorno=campo0.toInt();

  }

  return retorno;
}

#endif
