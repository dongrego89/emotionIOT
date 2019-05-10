/**
  \file Interaccion.h
  \brief Definición de clase Interaccion
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef INTERACCION_H
#define INTERACCION_H

#include <ArduinoSTL.h>
#include <Iluminacion.h>
#include <Tonos.h>

using namespace std;

/**
Instancia un objeto Interaccion con las propiedades y características asociadas al mismo
*/

class Interaccion{
private:
  int sonido_;/** Sonido al ser pulsado */
  vector<int> pinLed_;/** Pines de salida correspondientes a los led a utilizar en efecto_ */
  int iluminacion_;/** Efecto de iluminación a reproducir */
  int retardo_;/** Pausa tras mostrar la pantalla asociada al botón */

public:

/** Métodos Constructores */
/**
   \brief Constructor vacío de clase
*/
  Interaccion(){};

/**
    \brief Constructor de clase
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param retardo Tiempo que se mostrará la pantalla
*/
  Interaccion(int sonido,vector<int> pinLed,int iluminacion,int retardo){
    this->setValores(sonido,pinLed,iluminacion,retardo);
  }

/**
    \brief Constructor de clase
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param retardo Tiempo que se mostrará la pantalla
*/
  Interaccion(String sonido,vector<String> pinLed,String iluminacion,String retardo){
    this->setValores(sonido,pinLed,iluminacion,retardo);
  }

/** Métodos Inicializadores */
/**
    \brief Inicializador de valores
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param retardo Tiempo que se mostrará la pantalla
*/
  virtual void setValores(int sonido,vector<int> pinLed,int iluminacion,int retardo){
    this->sonido_=sonido;
    this->pinLed_=pinLed;
    this->iluminacion_=iluminacion;
    this->retardo_=retardo;
    }

/**
    \brief Inicializador de valores
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param retardo Tiempo que se mostrará la pantalla
*/
  virtual void setValores(String sonido,vector<String> pinLed,String iluminacion,String retardo){
    vector<int> pinLedAux;

    for(int i=0;i<(int)pinLed.size();i++){
      pinLedAux.push_back(pinLed[i].toInt());
    }

    this->setValores(sonido.toInt(),pinLedAux,iluminacion.toInt(),retardo.toInt());
  }

/** Métodos Observadores */

/**
\brief Observador de variable sonido_
\return Contenido de la variable sonido_
*/
int getSonido(){
  return this->sonido_;
}
/**
\brief Observador del vector pinLed_
\return Contenido del vector pinLed_
*/
vector<int> getPinLed(){
  return this->pinLed_;
}
/**
\brief Observador de variable iluminacion_
\return Contenido de la variable iluminacion_
*/
int getIluminacion(){
  return this->iluminacion_;
}

/**
   \brief Observador de variable retardo_
   \return Contenido de la variable retardo_
*/
int getRetardo(){
  return this->retardo_;
}


/**
   \brief Reproduce las interacciones multimedia de sonido e iluminación
*/
void reproducirInteraccion(){
  this->reproducirIluminacion();
  this->reproducirSonido();

}

/**
   \brief Reproduce la interacción de iluminación
*/
void reproducirIluminacion(){
  iluminacion(this->getPinLed(),this->getIluminacion());
}

/**
 \brief Reproduce la interacción de sonido
*/
void reproducirSonido(){
  sonido(this->getSonido());
}


};

#endif
