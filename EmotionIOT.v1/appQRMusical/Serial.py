import sys, time, serial
import threading

from appQRMusical.Audio import *
from appQRMusical.Funciones import *
from . import global_vars
from django.conf import settings


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


conexionArduino=conexionSerial("/dev/ttyACM0",9600,1,)

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
	@param conexionArduino Conexión Serial inicializada
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
	@param conexionArduino Conexión Serial inicializada
	"""
	hiloSerial=threading.Thread(name="hiloSerial",target=escuchaSerial,args=(conexionArduino,))
	hiloSerial.start()
