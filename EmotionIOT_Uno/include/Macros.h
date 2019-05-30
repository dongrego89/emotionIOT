/**
   \file Macros.h
   \brief Definición de Macros para Arduino Uno
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef MACROS_H
#define MACROS_H

/** Librerías para el uso del lector RFID */
#include <SPI.h>
#include <MFRC522.h>

/** Pin SS para lector RFID */
#define SS_PIN 10
/** PIN RST para lector RFID */
#define RST_PIN 9

/** Declaración de objeto global RFID */
MFRC522 mfrc522(SS_PIN, RST_PIN);

/** Pin de salida para led verde*/
#define LEDVERDE 7

/** Pin de salida para led rojo*/
#define LEDROJO 6

/** Pin de salida para led de aviso*/
#define LEDAVISO 4

/** Pin de salida para zumbador */
#define ZUMBADOR 5

/** Efecto de iluminacion utilizado en lectura RFID*/
#define EFECTORFID 4

/** Tono utilizado en lectura RFID*/
#define TONORFID 16

/** Tono utilizado en lectura RFID*/
#define TIEMPORFID 600

#endif
