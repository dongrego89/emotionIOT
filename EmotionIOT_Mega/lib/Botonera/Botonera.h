/**
  \file Botonera.h
  \brief Definición de clase Botonera
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef BOTONERA_H
#define BOTONERA_H

#include <ArduinoSTL.h>
#include <Boton.h>
#include <Pantalla.h>

using namespace std;

/**
Instancia un objeto Botonera que contiene los distintos botones que componen la interfaz
*/

class Botonera{
private:
vector<Boton> botones_;/** Vector de botones */

public:
/** Métodos Constructores */
/**
   \brief Constructor vacío de clase
*/
Botonera(){};

/**
 \brief Constructor de clase
 \param botones_ Vector de botones que conforman la botonera
*/
Botonera(vector<Boton> botones_);

/** Métodos Inicializadores */

/**
 \brief Agrega un nuevo boton al vector botones_
 \param boton Boton para agregar al vector
*/
void setBoton(Boton boton){
  vector<Boton>::iterator i=botones_.begin();

  for(;i!=botones_.end();){
    if (i->getId()==boton.getId())
      i = botones_.erase(i);
    else
      ++i;
    }
  botones_.push_back(boton);
}

/**
   \brief Agrega un nuevo boton al vector botones_
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
void setBoton(int id,int pin,int sonido,vector<int> pinLed,int iluminacion,vector<int> pinVibracion,int vibracion,int retardo,Pantalla pantalla){
  Boton boton(id, pin, sonido, pinLed, iluminacion, pinVibracion,vibracion, retardo, pantalla);
  this->setBoton(boton);
}

/**
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
void setBoton(String id,String pin, String sonido,vector<String> pinLed,String iluminacion,vector<String> pinVibracion,String vibracion,String retardo,Pantalla pantalla){
  Boton boton(id,pin,sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
  this->setBoton(boton);
}

/** Métodos Observadores */
/**
   \brief Calcula el numero de botones que componen la botonera
   \return Numero de elementos del vector botones_
*/
int getSize(){
  return this->botones_.size();
}

/**
   \brief Observador del vector botones_
   \param id del boton
   \return Boton con identificador id_ del vector botones_
*/
Boton getBoton(int boton){
  for(int i=0;i<(int)this->botones_.size();i++){
    if(botones_[i].getId()==boton){
      return botones_[i];
      }
    }
  return botones_[boton];
}

/**
   \brief Observador del vector botones_
   \return Vector con botones
*/
vector<Boton> getBotones(){
  return this->botones_;
}

};

#endif
