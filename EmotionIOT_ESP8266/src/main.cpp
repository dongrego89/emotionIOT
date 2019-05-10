/**
   \file main.cpp
   \brief Definición del programa sketch para ESP8266
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#include <Macros.h>
#include <EntradaSerial.h>
#include <FuncionesMQTT.h>

void setup_wifi() {
  int i;
  delay(10);
  WiFi.mode(WIFI_STA);//Ultima adicion
  WiFi.begin(ssid, password);
  delay(REACCION);
  i=0;

  while (WiFi.status() != WL_CONNECTED) { //Mientras el estado de WiFi no sea CONECTADO
    if((i%5000)==0){ //Cada 5000 iteraciones
      Serial.print("2;;10,11;2;;;500;1;4;Conectando a;2;6;red WiFi;");
      i=0;
    }
    i++;

    //Parpadear el led de estado azul
    digitalWrite(LEDAZUL,LOW);
    delay(250);
    digitalWrite(LEDAZUL,HIGH);
    delay(250);
  }

  digitalWrite(LEDAZUL,HIGH); //Una vez el estado de WiFi sea CONECTADO, encender el led azul

  randomSeed(micros());

  Serial.print("2;10;10;2;;;500;1;3;Conexion WiFi;2;4;establecida;");
  delay(REACCION);

}

void setup() {

  //Configurar los pines de salida por defecto
  pinMode(LEDAZUL,OUTPUT);
  pinMode(LEDAMARILLO,OUTPUT);

  //Tiempo de setup del Arduino Mega
  delay(10000);

  //Inicializar puerto serie
  Serial.begin(9600);

  //Configurar wifi
  setup_wifi();

  //Configurar cliente MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}



void loop() {
  
  //Si el cliente MQTT no está conectado, reconectar
  if (!client.connected()) {
    reconnect(client);
  }
  //Mantener el loop de cliente MQTT
  client.loop();

  //Comprobar si se reciben datos por Serial
  if(procesarEntradaSerial(topic,payload)){
    //En caso de recibir datos, realizar la publicación MQTT
    client.publish(topic.c_str(),payload.c_str());
  }

}
