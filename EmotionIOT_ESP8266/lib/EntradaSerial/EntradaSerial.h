/**
   \file EntradaSerial.h
   \brief Definición de funciones procesamiento de mensajes Serial
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef ENTRADASERIAL_H
#define ENTRADASERIAL_H

/**
   \brief Procesa la linea de entrada serial volcándola en los parámetros topic y contenido
   \param topic Topic del mensaje
   \param contenido Contenido del mensaje
   \return Valor booleano en función de si hubo o no lectura de valores por serial
*/

bool procesarEntradaSerial(String & topic, String & contenido){
  char token=';';
  String data;

   if (Serial.available()){
    data = Serial.readStringUntil('\n');
    data.trim();
    topic=data.substring(0,data.indexOf(token));
    data=data.substring(topic.length()+1);

    contenido=data.substring(0,data.indexOf(token));
    data=data.substring(contenido.length()+1);
    return true;
   }
   return false;
}

#endif
