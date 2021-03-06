/**
  \file LectorRFID.h
  \brief Funciones de manejo del lector RFID
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef LECTORRFID_H
#define LECTORRFID_H

#include <ArduinoSTL.h>
#include <sstream>
#include <iomanip>
#include <algorithm>

#include <Interaccion.h>
#include <Pantalla.h>

using namespace std;

/**
   \brief Convierte un número entero hexadecimal en formato de cadena
   \param num Número a convertir
   \return Cadena de texto con el número hexadecimal en formato cadena
*/
String intToHex(int num){
  stringstream ss;

  ss << hex << num;
  string res = ss.str();
  transform(res.begin(), res.end(),res.begin(), ::toupper);
  return String(res.c_str());
}

/**
   \brief Convierte un número entero hexadecimal en formato de cadena
   \param buffer Puntero al buffer que contiene el código RFID
   \param bufferSize Tamaño del buffer
   \param interaccionRFID Objeto de tipo interaccion
*/
void imprimirArray(byte *buffer, byte bufferSize,Interaccion & interaccionRFID){
  String codigo="";
  String valorAux;

  Pantalla pantallaAuxiliar;

  for (byte i = 0; i < bufferSize; i++){
    if(i!=0){
      codigo+=buffer[i] < 0x10 ? "0" : ":";
    }
    valorAux=buffer[i];
    codigo+=intToHex(valorAux.toInt());
  }
  pantallaAuxiliar=interaccionRFID.getPantalla();
  pantallaAuxiliar.setLinea(codigo,4,2);
  interaccionRFID.setPantalla(pantallaAuxiliar);
  codigo="Tarjeta;" + codigo + ";";
  Serial.println(codigo);
}

/**
   \brief Convierte un número entero hexadecimal en formato de cadena
   \param interaccionRFID Objeto de tipo interaccion
   \return Valor booleano en caso de que exista una lectura de tarjeta RFID
*/
bool deteccionTarjeta(Interaccion & interaccionRFID){
  if (mfrc522.PICC_IsNewCardPresent()){
    if (mfrc522.PICC_ReadCardSerial()){
      imprimirArray(mfrc522.uid.uidByte, mfrc522.uid.size, interaccionRFID);
      mfrc522.PICC_HaltA();
      return true;
    }
  }
  return false;
}

#endif
