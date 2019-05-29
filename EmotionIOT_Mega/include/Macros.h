/**
   \file Macros.h
   \brief Definición de Macros para Arduino Mega
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef MACROS_H
#define MACROS_H

/** Librerías para el uso de la pantalla LCD */
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

/** Librerías para el uso del lector RFID */
#include <SPI.h>
#include <MFRC522.h>

/** Pin SS para lector RFID */
#define SS_PIN 53
/** PIN RST para lector RFID */
#define RST_PIN 5


/** Pin de salida para zumbador */
#define ZUMBADOR 9
/** Pin de salida para motores de vibración*/
#define MOTOR 7
/** Pin de salida para led de estado verde*/
#define LEDVERDE 10
/** Pin de salida para led de estado rojo*/
#define LEDROJO 11


/** Pin de entrada para botón 1*/
#define BOTON1 22
/** Pin de entrada para botón 2*/
#define BOTON2 24
/** Pin de entrada para botón 3*/
#define BOTON3 26
/** Pin de entrada para botón 4*/
#define BOTON4 28


/** Pin inicial abierto para entrada de botones*/
#define BOTONINICIO 22

/** Pin final abierto para entrada de botones*/
#define BOTONFIN 40

/** Pines inicial abierto para salida de señales*/
#define SALIDAINICIO 41

/** Pines final abierto para salida de señales*/
#define SALIDAFIN 49

/** Efecto de iluminacion utilizado en lectura RFID*/
#define EFECTORFID 4

/** Tono utilizado en lectura RFID*/
#define TONORFID 16

/** Tono utilizado en lectura RFID*/
#define TIEMPORFID 600

/** Tiempo por defecto para interaccion */
#define TIEMPOINTERACCION 1000


/** Declaración de objeto global RFID */
MFRC522 mfrc522(SS_PIN, RST_PIN);

/** Declaración de objeto global LCD */
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 4 line display

#endif
