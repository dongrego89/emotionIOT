import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import threading

from . import global_vars
from appQRMusical.Funciones import *

Respuestas = ("2;3;11;2;7;3;2000;","2;1;10;1;;;2000;","0;","2;2;10,11;2;;;5000;","2;15;41;5;;;1500;","2;0;41;6;;;0;","2;2;10;3;;;2000;")

def iniciarPilaDePublicacionMQTT():
	while True:
		if len(global_vars.pilaPublicacionesMQTT) > 0:
			publicacion=global_vars.pilaPublicacionesMQTT.pop(0)
			publicarMQTT(publicacion[0],publicacion[1],publicacion[2])
			time.sleep(4)

def cargarPublicacionesMQTT(listaPublicaciones):
	global_vars.pilaPublicacionesMQTT.extend(listaPublicaciones)

def publicarMQTT(topic,mensaje,plantilla):
	hiloPublicacion=threading.Thread(name="hiloPublicacion",target=publicarMensaje,args=(topic,mensaje,plantilla,))
	hiloPublicacion.start()

def publicarMensaje(topic,mensaje,plantilla):
	mensaje=Respuestas[plantilla] + mensaje
	publish.single(topic,payload=mensaje,qos=1,retain=False,will=None,auth=None,tls=None,transport="tcp")


def on_message(client, userdata, message):
	"""!
	@brief Función de callback al mensaje recibido por MQTT
	@param client Instancia cliente MQTT para esta función
	@param userdata Datos privados de usuario en instancia de objeto client
	@param message Mensaje MQTT recibido
	"""

	topic=formateaCodigo(message.topic)

	if topic == "Boton":
		valor=formateaCodigo(str(message.payload.decode("utf-8")))
		global_vars.boton=valor

	if topic == "Tarjeta":
		valor=formateaCodigoRFID(str(message.payload.decode("utf-8")))
		global_vars.tarjeta=global_vars.boton_mqtt=global_vars.message=valor

	print("\nMQTT: {}\nCodigo: {}\n".format(topic,valor))

def conexionMQTT(servidor,topics):
	"""!
	@brief Función abre una conexión de escucha MQTT
	@param servidor Dirección IP del servidor broker MQTT
	@param topics Topics a los que está subscrito el cliente MQTT
	"""

	mensaje=lineaCentrada(1,"EmotionIOT") + lineaCentrada(2,"Controller")

	cargarPublicacionesMQTT([("Pantalla",mensaje,2)])

	#Instancia del objeto cliente
	cliente = mqtt.Client(client_id="P1",clean_session=True,userdata=None,transport="tcp")
	#Numero maximo de mensajes QOS>0 que pueden fluir por la red a la vez. por defecto es 20
	cliente.max_inflight_messages_set(1)
	#Numero maximo de mensajes QOS>0 salientes esperando en cola
	cliente.max_queued_messages_set(10)
	#Establece el tiempo antes de reintentar un mensaje QOS>0 si el broker no responde
	cliente.message_retry_set(1)

	#Definir la función de callback al recibir mensaje entrante
	cliente.on_message=on_message

	print("\nMQTT Conectando a Broker : " + servidor + "\n")

	cliente.connect(servidor,port=1883, keepalive=60)

	mensaje="Suscribiendo a topics :"

	for i in topics:
		cliente.subscribe(i)
		mensaje = mensaje + "\n - " + i

	print(mensaje)

	cliente.loop_forever()



def arranqueMQTT(topics):
	"""!
	@brief Función que libera un hilo que arranca el servicio cliente MQTT
	@param topics Topics a los que suscribir el cliente MQTT
	"""
	hiloMQTT=threading.Thread(name="hiloMQTT",target=conexionMQTT,args=("127.0.0.1",topics,))
	hiloMQTT.start()

	hiloPublicacionesMQTT=threading.Thread(name="hiloPublicacionesMQTT",target=iniciarPilaDePublicacionMQTT,args=())
	hiloPublicacionesMQTT.start()

def encenderAvisoMQTT():
	mensaje=lineaCentrada(1,"Acerca la tarjeta") + lineaCentrada(2,"al lector RFID")
	cargarPublicacionesMQTT([("Pantalla",mensaje,4)])

def apagarAvisoMQTT():
	cargarPublicacionesMQTT([("Pantalla","",5)])
