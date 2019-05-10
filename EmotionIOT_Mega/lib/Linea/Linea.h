/**
  \file Linea.h
  \brief Definición de clase Linea
  \author Gregorio Corpas Prieto
  \date 13/03/2019
*/

#ifndef LINEA_H
#define LINEA_H

using namespace std;

/**
Instancia un objeto con las características necesarias para escribir una linea en una pantalla LCD
*/

class Linea{
private:
  String texto_;  /** Texto de la linea */
  int margen_;  /** Margen respecto al comienzo de la linea desde la izquierda */
  int fila_;  /** Identificador de fila */
public:

/** Métodos Constructores */

/**
   \brief Constructor vacío de clase
*/
Linea(){};
/**
   \brief Constructor de clase
   \param texto Texto de la linea
   \param margen Margen izquierdo para el texto de linea
   \param fila Identificador para la Linea
*/
Linea(String texto, int margen, int fila){
  this->texto_=texto;
  this->margen_=margen;
  this->fila_=fila;
}

/**
   \brief Constructor de clase
   \param texto Texto de la linea
   \param margen Margen izquierdo para el texto de linea
   \param fila Identificador para la Linea
*/
Linea(String texto, String margen, String fila){
  this->texto_=texto;
  this->margen_=margen.toInt();
  this->fila_=fila.toInt();
}

/** Métodos Inicializadores */

/**
   \brief Inicializador de variable texto_
   \param texto Texto a inicializar
   \post texto_ será inicializado
*/
void setTexto(String texto){
  this->texto_=texto;
}
/**
   \brief Inicializador de variable margen_
   \param margen Margen izquierdo
   \post margen_ será inicializado
*/
void setMargen(int margen){
  this->margen_=margen;
}
/**
   \brief Inicializador de variable fila_
   \param fila Identificador para la Linea
   \post fila_ será inicializado
*/
void setFila(int fila){
  this->fila_=fila;
}

/** Métodos Observadores */

/**
   \brief Observador de variable texto_
   \return Contenido de la variable texto_
*/
String getTexto(){ return this->texto_; }

/**
   \brief Observador de variable margen_
   \return Contenido de la variable margen_
*/
int getMargen(){
  return this->margen_;
}

/**
   \brief Observador de variable fila_
   \return Contenido de la variable fila_
*/
int getFila(){
  return this->fila_;
}

};

#endif
