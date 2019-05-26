from appEmotionIOT.GoogleTTS import *

import pygame
from pygame import mixer
import threading

from . import global_vars

pygame.mixer.init(frequency=24000, size=-16, channels=2, buffer=4096)
pygame.init()

def iniciarPilaDeAudios():
    """!
    @brief Función que inicia un bucle permanente para procesar la pila de audios pendientes
    """
    while True:

        if len(global_vars.pilaSonidos) > 0:
            pygame.mixer.music.load(global_vars.pilaSonidos.pop()) #Cargar el primer elemento de la lista
            pygame.mixer.music.play() #Reproducir el elemento

            pendiente=True

            while len(global_vars.pilaSonidos)>=1 or pendiente:
                pygame.mixer.music.set_endevent(pygame.USEREVENT) #Establecer evento de fin de reproducción
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT: #Si la pista ha terminado
                        print("Fin de pista de audio")
                        if len ( global_vars.pilaSonidos ) >=1: #Si quedan pistas por reproducir el la lista
                            pygame.mixer.music.load(global_vars.pilaSonidos.pop()) #Cargar la siguiente pista
                            pygame.mixer.music.play() #Reproducir la pista
                        else:
                            pendiente=False
                            if(global_vars.numeroSonidosParaCargar > 1):
                                global_vars.ultimoSonidoPila = True

                        global_vars.primerSonidoPila = True




def arranqueReproductor():
    """!
    @brief Función que libera un hilo que arranca el reproductor de audios
    """
    hiloReproductor=threading.Thread(name="hiloReproductor",target=iniciarPilaDeAudios,args=())
    hiloReproductor.start()

def vaciarPilaAudios():
    """!
    @brief Función que limpia la pila actual de audios
    """
    global_vars.pilaSonidos.clear()

def cargarAudios(listaAudios):
    """!
    @brief Función que anexa a la pila actual de audios, los audios pasados por parámetro
    @param listaSonidos Lista de audios a añadir a la pila del sistema
    """
    global_vars.numeroSonidosParaCargar = len(listaAudios)
    global_vars.primerSonidoPila = False
    global_vars.ultimoSonidoPila = False
    global_vars.pilaSonidos.extend(listaAudios)


def narrarTTS(textos):
    """!
    @brief Función que transforma la lista de textos pasada por parámetro en archivos de audio y luego los carga en la pila
    @param textos Lista de textos a convertir en audios
    """
    vaciarPilaAudios()
    listaAudios=list()

    for i in textos:
        listaAudios.append(tts(i))

    listaAudios.reverse()

    cargarAudios(listaAudios)

def lanzarNarracion(textos):
    """!
    @brief Función que libera un hilo que invoca a la función de narración de textos
    @param textos Lista de textos a narrar
    """
    hiloNarracion=threading.Thread(name="hiloNarracion",target=narrarTTS,args=(textos,))
    hiloNarracion.start()
