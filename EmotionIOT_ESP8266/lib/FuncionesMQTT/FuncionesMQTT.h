/**
   \file FuncionesMQTT.h
   \brief Definición de funciones procesamiento de mensajes Serial
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef FUNCIONES_MQTT_H
#define FUNCIONES_MQTT_H

#include <PubSubClient.h>

/**
    \brief Callback de mensaje MQTT
    \param topic Topic del mensaje
    \param payload Contenido del mensaje
    \param length Longitud del mensaje completo MQTT
*/
void callback(char* topic, byte* payload, unsigned int length) {
  for (int i = 0; i < (int)length; i++) {
    Serial.print((char)payload[i]);
  }
}

/**
    \brief Reconexión del cliente MQTT
    \param client Cliente MQTT
*/
void reconnect(PubSubClient & client) {
  // Mientras que el cliente no esté conectado
  while (!client.connected()) {

    digitalWrite(LEDAMARILLO,LOW);

    // Crear random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str()),NULL,NULL,"Estado",0,0,"Conectado",true) {

      //Resuscribir al topic principal
      if(!client.subscribe("Pantalla")){
        Serial.print("2;11;11;3;;;500;1;3;Error conexion;2;8;MQTT;");
        delay(RECONEXION_MQTT);
        }

    }
    else{
      Serial.print("2;11;11,10;3;;;500;1;4;Reconectando;2;8;MQTT;");
      delay(REACCION);

      // Esperar i segundos antes de reintentar
      for(int i=0;i<5;i++){
        digitalWrite(LEDAMARILLO,HIGH);
        delay(500);
        digitalWrite(LEDAMARILLO,LOW);
        delay(500);
      }
    }
  }
  // Una vez reconectado, publicar un aviso
  Serial.print("2;10;10;2;;;500;1;3;Conexion MQTT;2;4;establecida;");
  digitalWrite(LEDAMARILLO,HIGH);
  delay(REACCION);

}


#endif
