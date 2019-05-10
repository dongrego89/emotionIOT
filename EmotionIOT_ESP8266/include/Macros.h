/**
   \file Macros.h
   \brief Definición de Macros para ESP8266
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef MACROS_H
#define MACROS_H

/** Librería para el uso de antena WiFi */
#include <ESP8266WiFi.h>

/** Librería para el uso del protocolo MQTT */
#include <PubSubClient.h>

/** Librería para el uso de antena WiFi */
#include <stdlib.h>


/** Pin de salida para led de estado azul*/
#define LEDAZUL 5

/** Pin de salida para led de estado amarillo*/
#define LEDAMARILLO 4

/** Pausas entre escrituras serial */
#define REACCION 2000

/** Cadena para almacenar los topics de los mensajes MQTT */
String topic;

/** Cadena para almacenar los payload de los mensajes MQTT */
String payload;

/** Configuración router OVISLINK*/

const char* ssid = "EmotionIOT-Network";
const char* password = "InternetOfThings";
const char* mqtt_server = "192.168.0.50";


/** Configuración pruebas en casa*/
/*
const char* ssid = "TVALCOLEA_CP";
const char* password = "123tvalcolea";
const char* mqtt_server = "192.168.2.130";
/** Configuración pruebas en departamento*/
/*
const char* ssid = "UCOTEAM";
const char* password = "-polonio210alfileres-";
const char* mqtt_server = "192.168.1.64";
*/


/** Instancia de objeto cliente WiFi */
WiFiClient espClient;

/** Instancia de objeto cliente MQTT */
PubSubClient client(espClient);

#endif
