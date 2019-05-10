/**
   \file Pantalla.h
   \brief Definición de clase Pantalla
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef PANTALLA_H
#define PANTALLA_H

#include <ArduinoSTL.h>
#include <Linea.h>

using namespace std;

/**
Instancia un objeto con las características necesarias para configurar una pantalla LCD de varias líneas
*/

class Pantalla{
private:
 vector<Linea> lineas_;/** Vector de lineas que conforman la pantalla */
public:

/** Métodos Constructores */
/**
   \brief Constructor vacío de clase
*/
Pantalla(){};

 /**
    \brief Constructor de clase
    \param lineas a almacenar en el vector
 */
Pantalla(vector<Linea> lineas){
  this->lineas_=lineas;
}


/** Métodos Inicializadores */

/**
   \brief Agrega una linea al vector lineas_
   \param lineas_ Vector de lineas que conforman el objeto Pantalla
*/
void setPantalla(vector<Linea> lineas){
  this->lineas_=lineas;
}

 /**
    \brief Agrega una linea al vector lineas_
    \param texto Texto de la linea
    \param margen Margen izquierdo para el texto de linea
    \param fila Identificador para la Linea
 */
void setLinea(String texto, int margen, int fila){
 Linea linea(texto,margen,fila);
  this->setLinea(linea);
}

 /**
    \brief Agrega una linea al vector lineas_
    \param texto Texto de la linea
    \param margen Margen izquierdo para el texto de linea
    \param fila Identificador para la Linea
 */
void setLinea(String texto, String margen, String fila){
 Linea linea(texto,margen.toInt(),fila.toInt());
 this->setLinea(linea);
}

/**
   \brief Agrega una linea al vector lineas_
   \param linea Linea de texto a añadir
*/
void setLinea(Linea & linea){
  vector<Linea>::iterator i=lineas_.begin();

  for(;i!=lineas_.end();){
    if (i->getFila()==linea.getFila())
      i = lineas_.erase(i);
    else
      ++i;
  }
  lineas_.push_back(linea);

}

/** Otros Métodos */

/**
   \brief Imprime las lineas del vector lineas_ por pantalla LCD
   \post Impresión de las lineas en la pantalla LCD
*/
void print(){
  if(this->lineas_.size()){
    this->clear();

    for(int i=0;i<(int)lineas_.size();i++){
      lcd.setCursor(lineas_[i].getMargen(),lineas_[i].getFila());
      lcd.print(lineas_[i].getTexto());
    }
  }
}

/**
   \brief Limpia la pantalla LCD
   \post Pantalla LCD en blanco
*/
void clear(){
  lcd.clear();
}

/**
   \brief Elimina todos los elementos linea del vector lineas_
   \post Vector _lineas vacío
*/
void vaciar(){
  this->lineas_.clear();
}

};

#endif
