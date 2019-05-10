/**
  \file Interaccion.h
  \brief Definición de clase Interaccion
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef INTERACCION_H
#define INTERACCION_H

#include <ArduinoSTL.h>
#include <Pantalla.h>
#include <Iluminacion.h>
#include <Tonos.h>
#include <Vibracion.h>

using namespace std;

/**
Instancia un objeto Interaccion con las propiedades y características asociadas al mismo
*/

class Interaccion{
private:
  int sonido_;/** Sonido al ser pulsado */
  vector<int> pinLed_;/** Pines de salida correspondientes a los led a utilizar en efecto_ */
  int iluminacion_;/** Efecto de iluminación a reproducir */
  vector<int> pinVibracion_;/** Pines de salida correspondientes a los motores a utilizar en vibracion_ */
  int vibracion_;/** Efecto de vibracion entre 0 y 255 */
  int retardo_;/** Pausa tras mostrar la pantalla asociada al botón */
  Pantalla pantalla_;/** Pantalla asociada al boton */

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
    \param pinVibracion Vector de pines de salida para efecto de vibracion
    \param vibracion Efecto de vibracion
    \param retardo Tiempo que se mostrará la pantalla
    \param pantalla Pantalla asociada a la interacción
*/
  Interaccion(int sonido,vector<int> pinLed,int iluminacion,vector<int> pinVibracion,int vibracion,int retardo,Pantalla pantalla){
    this->setValores(sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
  }

/**
    \brief Constructor de clase
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param pinVibracion Vector de pines de salida para efecto de vibracion
    \param vibracion Efecto de vibracion
    \param retardo Tiempo que se mostrará la pantalla
    \param pantalla Pantalla asociada a la interacción
*/
  Interaccion(String sonido,vector<String> pinLed,String iluminacion,vector<String> pinVibracion,String vibracion,String retardo,Pantalla pantalla){
    this->setValores(sonido,pinLed,iluminacion,pinVibracion,vibracion,retardo,pantalla);
  }

/** Métodos Inicializadores */
/**
    \brief Inicializador de valores
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param pinVibracion Vector de pines de salida para efecto de vibracion
    \param vibracion Efecto de vibracion
    \param retardo Tiempo que se mostrará la pantalla
    \param pantalla Pantalla asociada a la interacción
*/
  virtual void setValores(int sonido,vector<int> pinLed,int iluminacion,vector<int> pinVibracion,int vibracion,int retardo,Pantalla pantalla){
    this->sonido_=sonido;
    this->pinLed_=pinLed;
    this->iluminacion_=iluminacion;
    this->pinVibracion_=pinVibracion;
    this->vibracion_=vibracion;
    this->retardo_=retardo;
    this->pantalla_=pantalla;
    }

/**
    \brief Inicializador de valores
    \param sonido Sonido a reproducir
    \param pinLed Vector de pines de salida para efecto luminoso
    \param iluminacion Efecto luminoso
    \param pinVibracion Vector de pines de salida para efecto de vibracion
    \param vibracion Efecto de vibracion
    \param retardo Tiempo que se mostrará la pantalla
    \param pantalla Pantalla asociada a la interacción
*/
  virtual void setValores(String sonido,vector<String> pinLed,String iluminacion,vector<String> pinVibracion,String vibracion,String retardo,Pantalla pantalla){
    vector<int> pinLedAux, pinVibracionAux;

    for(int i=0;i<(int)pinLed.size();i++){
      pinLedAux.push_back(pinLed[i].toInt());
    }

    for(int i=0;i<(int)pinVibracion.size();i++){
      pinVibracionAux.push_back(pinVibracion[i].toInt());
    }

    this->setValores(sonido.toInt(),pinLedAux,iluminacion.toInt(),pinVibracionAux,vibracion.toInt(),retardo.toInt(),pantalla);
  }

/**
   \brief Inicializar pantalla
   \param pantalla Objeto pantalla
*/
void setPantalla(Pantalla & pantalla){
  this->pantalla_=pantalla;
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
\brief Observador del vector pinVibracion_
\return Contenido del vector pinVibracion_
*/
vector<int> getPinVibracion(){
  return this->pinVibracion_;
}
/**
   \brief Observador de variable vibracion_
   \return Contenido de la variable vibracion_
*/
int getVibracion(){
  return this->vibracion_;
}
/**
   \brief Observador de variable retardo_
   \return Contenido de la variable retardo_
*/
int getRetardo(){
  return this->retardo_;
}
/**
   \brief Observador de variable pantalla_
   \return Contenido de la variable pantalla_
*/
Pantalla getPantalla(){
  return this->pantalla_;
}

/**
   \brief Reproduce las interacciones multimedia de sonido e iluminación
*/
void reproducirInteraccion(){
  this->reproducirIluminacion();
  this->reproducirVibracion();
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
/**
 \brief Reproduce la interacción de vibracion
*/
void reproducirVibracion(){
  vibracion(this->getPinVibracion(),this->getVibracion());
}

};

#endif
