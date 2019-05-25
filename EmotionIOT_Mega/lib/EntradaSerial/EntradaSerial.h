/**
   \file EntradaSerial.h
   \brief Definición de funciones procesamiento de mensajes Serial
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef ENTRADASERIAL_H
#define ENTRADASERIAL_H

#include <ArduinoSTL.h>

#include <Interaccion.h>
#include <Pantalla.h>
#include <Boton.h>

/**
   \brief Procesa la linea de entrada serial y la transforma en el objeto correspondiente
   \param interaccionMQTT Objeto de interaccion procedente de loop
   \param pantalla Objeto de tipo pantalla
   \param boton Objeto de tipo boton
   \return Número con el código del elemento que ha sido procesado
*/

int entradaSerial(Interaccion & interaccionMQTT, Pantalla & pantallaInicio, Boton & nuevoBoton){
  char token1=';';
  char token2=',';

  int retorno=0;

  String data1, data2, campo0, campo1, campo2, campo3, campo4, campo5, campo6, campo7, campo8, campo9, campo10, campo11, campo12;
  Pantalla pantalla;

  vector<String> pinLed, pinVibracion;

  if (Serial.available()){
    data1 = Serial.readStringUntil('\n');
    data1.trim();

    //Procesamiento del tipo de mensaje
    campo0=data1.substring(0,data1.indexOf(token1));
    data1=data1.substring(campo0.length()+1);


    switch(campo0.toInt()){
      case 0://Configuracion del standby
        /**
        Formato:
        Codigo;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;

        Ejemplo:
        0;0;4;Primera Fila;1;5;Segunda Fila;2;6;Tercera Fila;3;6;Cuarta Fila;
        */

        //Borrar lineas anteriores
        pantallaInicio.vaciar();

        //Procesamiento del mensaje para reproducir por pantalla
        while(data1.length()>1){
          campo1=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo1.length()+1);

          campo2=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo2.length()+1);

          campo3=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo3.length()+1);

          pantallaInicio.setLinea(campo3,campo2,campo1);
        }
          return 1; //Instruccion de pantalla de inicio

      break;

      case 1://Configuración de botones
      /**
      Formato:
      Codigo;Id;PinHW;Sonido;PinLed1,PinLed2;Iluminacion;PinVib1,PinVib2;Vibracion;Retardo;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;
      Ejemplo:
      1;1;22;2;10,11;2;7;1;1000;2;0;0;Primera Linea;1;0;Segunda Linea;2;0;Tercera Linea;3;0;Cuarta Linea;
      */


        //Id
        campo11=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo11.length()+1);

        //Pin hardware
        campo12=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo12.length()+1);

        //Sonido
        campo1=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo1.length()+1);

        //PinLed
        campo2=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo2.length()+1);

        data2=campo2;

        while(data2.length()>=1){
          campo3=data2.substring(0,data2.indexOf(token2));
          data2=data2.substring(campo3.length()+1);
          pinLed.push_back(campo3);

        }

        //Iluminacion
        campo4=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo4.length()+1);

        //PinVibracion
        campo5=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo5.length()+1);

        data2=campo5;

        while(data2.length()>=1){
          campo3=data2.substring(0,data2.indexOf(token2));
          data2=data2.substring(campo3.length()+1);
          pinVibracion.push_back(campo3);
        }

        //Vibracion
        campo6=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo6.length()+1);

        //Delay
        campo7=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo7.length()+1);


        //Si existe mensaje para reproducir por pantalla
        while(data1.length()>=1){
          campo8=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo8.length()+1);

          campo9=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo9.length()+1);

          campo10=data1.substring(0,data1.indexOf(token1));
          data1=data1.substring(campo10.length()+1);

          pantalla.setLinea(campo10,campo9,campo8);

        }

        nuevoBoton.setValores(campo11,campo12,campo1,pinLed,campo4,pinVibracion,campo6,campo7,pantalla);

        retorno=5;
      break;
      case 2://Llamada a interaccion MQTT de respuesta
      /**
      Formato:
      Codigo;Sonido;PinLed1,PinLed2;Iluminacion;PinVib1,PinVib2;Vibracion;Retardo;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;Fila;Margen;Texto;
      Ejemplo:
      2;1;10,11;2;7;1;1000;0;0;Primera Linea;1;0;Segunda Linea;2;0;Tercera Linea;3;0;Cuarta Linea;
      */

      //Sonido
      campo1=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo1.length()+1);

      //PinLed
      campo2=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo2.length()+1);

      data2=campo2;

      while(data2.length()>=1){
        campo3=data2.substring(0,data2.indexOf(token2));
        data2=data2.substring(campo3.length()+1);
        pinLed.push_back(campo3);
      }

      //Iluminacion
      campo4=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo4.length()+1);

      //PinVibracion
      campo5=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo5.length()+1);

      data2=campo5;

      while(data2.length()>=1){
        campo3=data2.substring(0,data2.indexOf(token2));
        data2=data2.substring(campo3.length()+1);
        pinVibracion.push_back(campo3);
        Serial.print(campo3+",");
      }


      //Vibracion
      campo6=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo6.length()+1);

      //Delay
      campo7=data1.substring(0,data1.indexOf(token1));
      data1=data1.substring(campo7.length()+1);

      //Si existe mensaje para reproducir por pantalla
      while(data1.length()>=1){
        campo8=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo8.length()+1);

        campo9=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo9.length()+1);

        campo10=data1.substring(0,data1.indexOf(token1));
        data1=data1.substring(campo10.length()+1);

        pantalla.setLinea(campo10,campo9,campo8);

      }

      interaccionMQTT.setValores(campo1,pinLed,campo4,pinVibracion,campo6,campo7,pantalla);

      retorno=4; //Instruccion de interaccion con MQTT

      break;

      default:
        retorno=0;
      break;
      }
  }

  return retorno;
}

#endif
