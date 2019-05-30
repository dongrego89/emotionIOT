"""!
@package Serial.py
@brief Archivo de funciones para manejo de Arduino por puerto Serie
@author Gregorio Corpas Prieto
@date 13/03/2019
"""
import sys, time, serial, serial.tools.list_ports, warnings
import threading

from appEmotionIOT.Audio import *
from appEmotionIOT.Funciones import *
from . import global_vars
from django.conf import settings


def listarPuertos():
    """!
    @brief Devuelve los nombres de los puertos serial que tienen un dispositivo Arduino conectado
    @return Tupla con la lista de puertos y la lista correspondiente a las descripciones de los dispositivos Arduino asociados
    """
    ports = list( serial.tools.list_ports.comports() )

    resultPorts = []
    descriptions = []
    for port in ports:
        if not port.description.startswith( "Arduino" ):
            # correct for the somewhat questionable design choice for the USB
            # description of the Arduino Uno
            if port.manufacturer is not None:
                if port.manufacturer.startswith( "Arduino" ) and \
                   port.device.endswith( port.description ):
                    port.description = "Arduino Uno"
                else:
                    continue
            else:
                continue
        if port.device:
            resultPorts.append( port.device )
            descriptions.append( str( port.description ) )

    return (resultPorts, descriptions)

def conexionSerial(puerto,baudios,timeout):
	"""!
	@brief Función que abre puerto de comunicación serial y si recibe cadenas las almacena variable global
	@param puerto Puerto serial de comunicación
	@param baudios Velocidad de transmisión
	@param timeout Tiempo de espera máximo para control de lectura
    """
	conexionArduino = serial.Serial(puerto, baudios, timeout=timeout)
	time.sleep(3)
	return conexionArduino

def encenderAvisoSerial():
	"""!
	@brief Función que activa el led de aviso del lector RFID Serial Arduino Uno
	"""
	if global_vars.avisoSerial==False:
		global_vars.avisoSerial=True
		conexionArduino.write(b'1;')
		music = settings.MEDIA_ROOT + '/songs/bloop.ogg'
		cargarAudios([music])

def apagarAvisoSerial():
	"""!
	@brief Función que apaga el led de aviso del lector RFID Serial Arduino Uno
	"""
	if global_vars.avisoSerial==True:
		global_vars.avisoSerial=False
		conexionArduino.write(b'2;')

def escuchaSerial(conexionArduino):
	"""!
	@brief Función que inicia un bucle permanente para la lectura de códigos RFID Serial Arduino Uno
	@param conexionArduino Objeto de conexión Serial inicializada
	"""
	codigo = 0
	while True:
		tag = conexionArduino.readline()
		codigo = tag.decode('utf-8')
		if hash(tag) != 0:
			global_vars.tarjeta=global_vars.message=global_vars.boton_mqtt=formateaCodigoRFID(codigo)
			print("\nSerial: {}\nCodigo: {}\n".format("Tarjeta",global_vars.message))


def arranqueSerial(conexionArduino):
	"""!
	@brief Función que libera un hilo que arranca la lectura de cadenas por puerto Serial
	@param conexionArduino Objeto de conexión Serial inicializada
	"""
	hiloSerial=threading.Thread(name="hiloSerial",target=escuchaSerial,args=(conexionArduino,))
	hiloSerial.start()
