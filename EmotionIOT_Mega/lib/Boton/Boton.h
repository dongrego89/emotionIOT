/**
  \file Boton.h
  \brief Definición de clase Boton
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef BOTON_H
#define BOTON_H

#include <Interaccion.h>

using namespace std;

/**
Instancia un objeto Boton que hereda de la clase Interaccion
*/

class Boton: public Interaccion{
private:
  int id_;/** Identificador */
  int pin_;/** Pin de entrada hardware */

public:
/** Métodos Constructores */
/**
   \brief Constructor vacío de clase
*/
Boton(){};

/**
    \brief Constructor de clase
    \param id Identificador del boton
    \param pin Pin de entrada hardware
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param pinVibracion Vector de pines de salida para efecto de vibracion
    \param vibracion Efecto de vibracion
    \param retardo Tiempo que se mostrará la pantalla
    \param pantalla Pantalla asociada a la interacción
*/
Boton(int id,int pin,int sonido,vector<int> pinLed,int iluminacion,vector<int> pinVibracion,int vibracion,int retardo,Pantalla pantalla){
  this->setValores(id,pin,sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
}

/**
   \brief Constructor de clase
   \param id Identificador del boton
   \param pin Pin de entrada hardware
   \param sonido Sonido a reproducir
   \param pinLed Vector de pines de salida para efecto luminoso
   \param iluminacion Efecto luminoso
   \param pinVibracion Vector de pines de salida para efecto de vibracion
   \param vibracion Efecto de vibracion
   \param retardo Tiempo que se mostrará la pantalla
   \param pantalla Pantalla asociada a la interacción
*/

Boton(String id,String pin,String sonido,vector<String> pinLed,String iluminacion,vector<String> pinVibracion,String vibracion,String retardo,Pantalla pantalla){
  this->setValores(id,pin,sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
}

/** Métodos Inicializadores */

/**
   \brief Inicializador de valores
   \param id Identificador del boton
   \param pin Pin de entrada hardware
   \param sonido Sonido a reproducir
   \param pinLed Vector de pines de salida para efecto luminoso
   \param iluminacion Efecto luminoso
   \param pinVibracion Vector de pines de salida para efecto de vibracion
   \param vibracion Efecto de vibracion
   \param retardo Tiempo que se mostrará la pantalla
   \param pantalla Pantalla asociada a la interacción
*/

void setValores(String id,String pin,String sonido,vector<String> pinLed,String iluminacion,vector<String> pinVibracion,String vibracion,String retardo,Pantalla pantalla){
  Interaccion::setValores(sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
  this->id_=id.toInt();
  this->pin_=pin.toInt();
}

/**
   \brief Inicializador de valores
   \param id Identificador del boton
   \param pin Pin de entrada hardware
   \param sonido Sonido a reproducir
   \param pinLed Vector de pines de salida para efecto luminoso
   \param iluminacion Efecto luminoso
   \param pinVibracion Vector de pines de salida para efecto de vibracion
   \param vibracion Efecto de vibracion
   \param retardo Tiempo que se mostrará la pantalla
   \param pantalla Pantalla asociada a la interacción
*/

void setValores(int id,int pin,int sonido,vector<int> pinLed,int iluminacion,vector<int> pinVibracion,int vibracion,int retardo,Pantalla pantalla){
  Interaccion::setValores(sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
  this->id_=id;
  this->pin_=pin;
}

/** Métodos Observadores */
/**
   \brief Observador de variable id_
   \return Contenido de la variable id_
*/
int getId(){
  return this->id_;
}
/**
   \brief Observador de variable pin_
   \return Contenido de la variable pin_
*/
int getPin(){
  return this->pin_;
}

};

#endif
