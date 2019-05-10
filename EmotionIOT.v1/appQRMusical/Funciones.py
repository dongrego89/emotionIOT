from math import *

def formateaCodigo(codigo):
	"""!
	@brief Función que recibe un código y elimina todos los caracteres de control
	@param codigo Código a formatear
	"""
	return codigo.rstrip().strip().lstrip()

def formateaCodigoRFID(codigo):
	"""!
	@brief Función que recibe un código RFID y elimina todos los caracteres de control y el caracter ':'
	@param codigo Código RFID a formatear
	"""
	return formateaCodigo(codigo).replace(":","")

def lineaCentrada(fila,texto):
	"""!
	@brief Función que construye una linea de texto centrada para pantalla LCD
	@param fila Índice de la fila
	@param texto Contenido de la línea de texto
	@return Línea de texto con formato para pantalla LCD
	"""
	caracteres=20
	margen=floor((caracteres-len(texto)) / 2)
	resultado=str(fila) + ";" + str(margen) + ";" + texto + ";"
	return resultado
