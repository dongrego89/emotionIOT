"""!
@package views.py
@brief Archivo de vistas
@author Gregorio Corpas Prieto
@date 13/03/2019
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from appQRMusical.GoogleTTS import *
from appQRMusical.Serial import *
from appQRMusical.Audio import *
from appQRMusical.MQTT import *

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime, time, date


#Users
from django.contrib.auth.models import User

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Play + Multimedia
from .models import Actividad
from . import global_vars

# Multimedia
from .models import Multimedia, Contenido, Actividad_Contenido, Pregunta_Quizz, Pregunta_Matching, Pregunta, Actividad_Pregunta
import os
from PIL import Image
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import UploadMultimediaForm

# Player
from .models import Actividad
from .forms import FormularioActividad
from django.urls import reverse_lazy, reverse

# Paciente
from .models import Paciente
from .forms import UploadUserForm

# Especialista
from .models import Especialista
from .forms import FormularioEspecialista

# Terapia
from .models import Terapia, Asigna_Terapia, Especialista_Asigna_Terapia, Terapia_Actividad
from .forms import UploadTherapyForm, UploadAsign, UploadTherapyFormActividad, UploadAsignTherapyForm, UploadOneActividadTherapyForm, UploadOnePlayerTerapiaForm

# Tratamiento
from .models import Tratamiento, Supervisa
from .forms import UploadTreatmentForm

# Diagnostico
from .models import Diagnostico
from .forms import UploadDiagnosticForm

# Indicador
from .models import Indicador
#, Terapia_Indicador
from .forms import UploadIndicatorForm

# Categoria
from .models import Categoria, Categoria_Actividad
from .forms import UploadCategoryForm, FormularioCategoriaActividad

#Sesion
from .models import Sesion, Resultado_Sesion

#Player Game
import threading
import subprocess
import time
import random


# User Settings
from .forms import EditNameForm, EditEmailForm, EditPassForm
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse


import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import threading

from math import *

from appQRMusical.Funciones import *








arranqueMQTT(("Boton","Tarjeta"))
arranqueSerial(conexionArduino)
arranqueReproductor()

def prueba(request):
	context = {}
	if request.method == "POST":
		context['titulo'] = "Recibido"
		return redirect('home')
	else:
		context['titulo'] = "Prueba"
		return render(request,'prueba.html',context)

class LoginPacientes(TemplateView):
	"""!
	@brief Vista de la pantalla de login para pacientes
	@param TemplateView Clase genérica de Django para las vistas
	"""
	global_vars.boton_mqtt=""
	template_name="loginPacientes.html"
	def get_context_data(self, **kwargs):
		context = super(LoginPacientes, self).get_context_data(**kwargs)
		try:
			player = Paciente.objects.get(online="si")
			apagarAvisoSerial()
		except Paciente.DoesNotExist:
			player = None
			encenderAvisoSerial()

		context['QRM_color'] = "QRM_blue"
		context['player'] = player
		context['titulo'] = "Login Pacientes"

		return context

def RFIDLogin(request):
	"""!
	@brief Función que desde segundo plano inicia sesión
	@param Petición web
	"""
	codigo=global_vars.tarjeta
	global_vars.tarjeta=None
	context={}

	if codigo:
		try:
			paciente = Paciente.objects.get(codigo=codigo)
			paciente.online = "si"
			paciente.save()
			context['redireccionar'] = True


		except Paciente.DoesNotExist:
			context['redireccionar'] = False
			context['codigoMQTT']= codigo
			context['mensaje'] = "No existe ningun usuario con el codigo"


	return JsonResponse(context)


def Desconectar(request):
	"""!
	@brief Función para desconexión de pacientes
	@param Petición web
	"""
	global_vars.boton_mqtt=""

	try:
		user = Paciente.objects.get(online="si")
		user.online = "no"
		user.save()

	except Paciente.DoesNotExist:

		user = None

	return redirect('/')




class ElegirTerapia(TemplateView):
	"""
	@brief Vista para elegir una terapia
	@param TemplateView Clase genérica de Django para las vistas
	"""

	template_name="elegirTerapia.html"
	model = Actividad.objects.all()
	def get_context_data(self, **kwargs):
		context = super(ElegirTerapia, self).get_context_data(**kwargs)
		try:
			paciente = Paciente.objects.get(online="si")
		except Paciente.DoesNotExist:
			paciente = None
			apagarAvisoSerial()
			return context

		apagarAvisoSerial()

		#Filtrar los tratamientos activos pertenecientes al paciente
		tratamientos = Tratamiento.objects.filter(activado=True).filter(paciente_id=paciente.id)

		#Tomar las terapias que coincidan con el filtrado previo
		asignaTerapias=Asigna_Terapia.objects.filter(tratamiento_id__in=tratamientos).values("id_asign_therapy","terapia","terapia__nombre")


		context['mensaje'] = "Selecciona una Terapia"
		context['mensaje_error'] = "No existen terapias disponibles"
		context['titulo'] = "Terapias"
		context['asignaTerapias'] = asignaTerapias
		context['QRM_color'] = "QRM_orange"
		context['player'] = paciente

		lanzarNarracion([context['mensaje']])

		apagarAvisoSerial()
		return context




#Vista de la elección de actividad una vez seleccionado terapia
def ElegirActividad(request, idTerapia, idAsignaTerapia):
	"""
	@brief Vista para elegir una actividad
	@param request Peticion http
	@param idTerapia Código de la terapia a la que pertenecen las actividades
	"""

	try:
		paciente = Paciente.objects.get(online="si")
	except Paciente.DoesNotExist:
		paciente = None
		apagarAvisoSerial()
		return context

	asignacionesActividades=Terapia_Actividad.objects.filter(terapia=idTerapia)
	actividades=Actividad.objects.filter(id__in=asignacionesActividades.values("actividad"))

	global_vars.game_initialized = False
	global_vars.quizzInicializado = False
	global_vars.matchingInicializado = False

	terapia=Terapia.objects.get(id=idTerapia)

	context = {}
	context['idTerapia'] = idTerapia
	context['idAsignaTerapia'] = idAsignaTerapia
	context['mensaje'] = "Selecciona una Actividad"
	context['mensaje_error'] = "No existen actividades disponibles"
	context['titulo'] =  "%s | %s" %  (terapia," Actividades")
	context['actividades'] = actividades
	context['QRM_color'] = "QRM_orange"
	context['player'] = paciente

	lanzarNarracion([context['mensaje']])

	apagarAvisoSerial()
	return render(request, 'elegirActividad.html', context)

def Matching(request,idActividad,idAsignaTerapia):
	"""!
	@brief Método para juegos tipo Matching
	@param request Peticion http
	@param idActividad Id de la actividad a realizar
	@param idAsignaTerapia Id de la tupla Asigna_Terapia para usar en la sesión
	"""
	context={}

	if global_vars.matchingInicializado == False:
		"""
		Inicialización de variables globales
		"""
		actividad=Actividad.objects.get(id=idActividad)

		global_vars.narrarPreguntas=actividad.narracion
		global_vars.indicePreguntaActual=0
		aleatorio=actividad.aleatorio

		preguntasDeActividad=Actividad_Pregunta.objects.filter(actividad=idActividad).values("pregunta__id")

		print(preguntasDeActividad)

		preguntasMatching=Pregunta_Matching.objects.filter(id__in=preguntasDeActividad)

		if(aleatorio): # Si la actividad ordena las preguntas aleatoriamente
			preguntasMatching=preguntasMatching.order_by('?')
		else: # Si usamos pila y pop para sacar las preguntas, habría que aplicar un reverse.
			preguntasMatching=preguntasMatching.order_by('id')

		global_vars.pilaPreguntas=list(preguntasMatching)

		print(global_vars.pilaPreguntas)

		for i in global_vars.pilaPreguntas:
			print("{}".format(i.pregunta))

		global_vars.indiceRespuesta=None
		global_vars.indicadorErrores=0
		global_vars.indicadorAciertos=0
		global_vars.indicadorTiempoInicio=time.time()
		global_vars.matchingInicializado = True
		global_vars.sesionGuardada = False

	if global_vars.indicePreguntaActual < len(global_vars.pilaPreguntas):
		"""
		Si aun quedan preguntas por responder
		"""
		global_vars.tarjeta=None

		preguntaMatching=global_vars.pilaPreguntas[global_vars.indicePreguntaActual]

		#Buscar
		global_vars.indiceRespuesta=preguntaMatching.multimediaCorrecto.codigo

		print("La respuesta correcta es: {}".format(global_vars.indiceRespuesta))

		if global_vars.narrarPreguntas:
			narracion=[preguntaMatching.pregunta]
			lanzarNarracion(narracion)

		context['titulo'] = "Matching | Pregunta: {} ({})".format(preguntaMatching.pregunta,global_vars.indiceRespuesta)
		context['pregunta'] = preguntaMatching.pregunta
		context['opcion'] = preguntaMatching.multimediaCorrecto
		context['codigo'] = preguntaMatching.multimediaCorrecto.codigo
		context['formato'] = preguntaMatching.formato
	else:
		"""
		Si ya se respondieron todas las preguntas
		"""
		vaciarPilaAudios()

		global_vars.indicadorTiempoFin=time.time()
		actividad = Actividad.objects.get(id=idActividad)

		music = settings.MEDIA_ROOT + '/songs/tada.ogg'
		cargarAudios([music])

		if global_vars.sesionGuardada == False:
			global_vars.indicadorTiempoTotal=round(global_vars.indicadorTiempoFin - global_vars.indicadorTiempoInicio,2)
			sesionActividad = Sesion()
			sesionActividad.asigna_Terapia = Asigna_Terapia.objects.get(id_asign_therapy=idAsignaTerapia)
			sesionActividad.save()

			indicadoresActividad=actividad.indicador.all()

			for i in indicadoresActividad:
				print("Indicador con id : ",i.id_indicador)
				resultadoSesion = Resultado_Sesion()
				resultadoSesion.sesion = Sesion.objects.get(id_sesion=sesionActividad.id_sesion)
				resultadoSesion.actividad = Actividad.objects.get(id=idActividad)

				if i.id_indicador == 4:
					resultadoSesion.resultado = global_vars.indicadorErrores
					print("Fallos")

				if i.id_indicador == 5:
					resultadoSesion.resultado = global_vars.indicadorAciertos
					print("Aciertos")


				if i.id_indicador == 6:
					resultadoSesion.resultado = global_vars.indicadorTiempoTotal
					print("Tiempo")

				resultadoSesion.indicador = Indicador.objects.get(id_indicador=i.id_indicador)
				print(resultadoSesion.resultado)
				resultadoSesion.save()
				global_vars.sesionGuardada=True


		context['resultados'] = True
		context['errores'] = global_vars.indicadorErrores
		context['aciertos'] = global_vars.indicadorAciertos
		context['tiempo'] = global_vars.indicadorTiempoTotal

		context['titulo'] = "Matching | {} | Resultados".format(actividad)

	return render(request,'match.html',context)

def MatchingCallBack(request):
	"""!
	@brief Función que procesa las respuestas del juego de matching
	@param request Peticion http
	"""
	context={}
	context['indicePreguntaActual'] = global_vars.indicePreguntaActual+1
	context['numeroTotalPreguntas'] = len(global_vars.pilaPreguntas)

	tarjeta = global_vars.tarjeta
	global_vars.tarjeta=None

	if tarjeta:
		context['tarjeta'] = tarjeta
		context['tiempoPausa'] = 500
		context['indiceRespuesta'] = global_vars.indiceRespuesta

		if formateaCodigo(tarjeta) == formateaCodigo(str(global_vars.indiceRespuesta)):

			global_vars.indicePreguntaActual+=1
			global_vars.indicadorAciertos+=1

			mensaje=lineaCentrada(1,"Respuesta") + lineaCentrada(2,"Correcta")
			publicarMQTT("Pantalla",mensaje,1)

			context['mensaje'] = "Respuesta correcta"
			#procesar información de respuesta correcta

			context['refrescar'] = True
			music = settings.MEDIA_ROOT + '/songs/correcto.ogg'
			cargarAudios([music])

		else:
			global_vars.indicadorErrores+=1

			mensaje=lineaCentrada(1,"Respuesta") + lineaCentrada(2,"Incorrecta")
			publicarMQTT("Pantalla",mensaje,0)


			context['mensaje'] = "Respuesta incorrecta"
			music = settings.MEDIA_ROOT + '/songs/incorrecto.ogg'
			cargarAudios([music])

	return JsonResponse(context)

def Quizz(request,idActividad,idAsignaTerapia):
	"""!
	@brief Método para juegos tipo Quizz
	@param request Peticion http
	@param idActividad Id de la actividad a realizar
	@param idAsignaTerapia Id de la tupla Asigna_Terapia para usar en la sesión
	"""
	context={}

	if global_vars.quizzInicializado == False:
		"""
		Inicialización de variables globales
		"""
		actividad=Actividad.objects.get(id=idActividad)

		global_vars.narrarPreguntas=actividad.narracion
		global_vars.indicePreguntaActual=0
		aleatorio=actividad.aleatorio

		preguntasDeActividad=Actividad_Pregunta.objects.filter(actividad=idActividad).values("pregunta__id")

		preguntasQuizz=Pregunta_Quizz.objects.filter(id__in=preguntasDeActividad)

		if(aleatorio): # Si la actividad ordena las preguntas aleatoriamente
			preguntasQuizz=preguntasQuizz.order_by('?')
		else: # Si usamos pila y pop para sacar las preguntas, habría que aplicar un reverse.
			preguntasQuizz=preguntasQuizz.order_by('id')

		global_vars.pilaPreguntas=list(preguntasQuizz)

		print(global_vars.pilaPreguntas)

		for i in global_vars.pilaPreguntas:
			print("{}".format(i.pregunta))

		global_vars.indiceRespuesta=None
		global_vars.indicadorErrores=0
		global_vars.indicadorAciertos=0
		global_vars.indicadorTiempoInicio=time.time()
		global_vars.quizzInicializado = True
		global_vars.sesionGuardada = True


	if global_vars.indicePreguntaActual < len(global_vars.pilaPreguntas):
		"""
		Si aun quedan preguntas por responder
		"""
		global_vars.boton=None

		preguntaQuizz=global_vars.pilaPreguntas[global_vars.indicePreguntaActual]
		opciones=list(preguntaQuizz.multimediaIncorrecto.all())
		opciones.append(preguntaQuizz.multimediaCorrecto)

		random.shuffle(opciones)

		global_vars.indiceRespuesta=opciones.index(preguntaQuizz.multimediaCorrecto)+1

		print("La respuesta correcta es: {}".format(global_vars.indiceRespuesta))

		if global_vars.narrarPreguntas:
			narracion=list()
			narracion.append(preguntaQuizz.pregunta)
			for num, i in enumerate(opciones, start=1):
				narracion.append("{},{}".format(str(num),i.nombre))
			lanzarNarracion(narracion)


		context['titulo'] = "Quizz | Pregunta: {} ({})".format(preguntaQuizz.pregunta,global_vars.indiceRespuesta)
		context['pregunta'] = preguntaQuizz.pregunta
		context['opciones'] = opciones
		context['opcionCorrecta'] = preguntaQuizz.multimediaCorrecto
		context['visualizacion'] = preguntaQuizz.visualizacion
		context['formato'] = preguntaQuizz.formato

	else:
		"""
		Si ya se respondieron todas las preguntas
		"""
		vaciarPilaAudios()

		global_vars.indicadorTiempoFin=time.time()
		indicadorTiempo=round(global_vars.indicadorTiempoFin - global_vars.indicadorTiempoInicio,2)
		actividad = Actividad.objects.get(id=idActividad)

		music = settings.MEDIA_ROOT + '/songs/tada.ogg'
		cargarAudios([music])

		if global_vars.sesionGuardada == False:
			sesionActividad = Sesion()
			sesionActividad.asigna_Terapia = Asigna_Terapia.objects.get(id_asign_therapy=idAsignaTerapia)
			sesionActividad.save()

			indicadoresActividad=actividad.indicador.all()

			for i in indicadoresActividad:
				print("Indicador con id : ",i.id_indicador)
				resultadoSesion = Resultado_Sesion()
				resultadoSesion.sesion = Sesion.objects.get(id_sesion=sesionActividad.id_sesion)
				resultadoSesion.actividad = Actividad.objects.get(id=idActividad)

				if i.id_indicador == 4:
					resultadoSesion.resultado = global_vars.indicadorErrores
					print("Fallos")

				if i.id_indicador == 5:
					resultadoSesion.resultado = global_vars.indicadorAciertos
					print("Aciertos")


				if i.id_indicador == 6:
					resultadoSesion.resultado = indicadorTiempo
					print("Tiempo")

				resultadoSesion.indicador = Indicador.objects.get(id_indicador=i.id_indicador)
				print(resultadoSesion.resultado)
				resultadoSesion.save()
				global_vars.sesionGuardada=True


		context['resultados'] = True
		context['errores'] = global_vars.indicadorErrores
		context['aciertos'] = global_vars.indicadorAciertos
		context['tiempo'] = indicadorTiempo

		context['titulo'] = "Quizz | {} | Resultados".format(actividad)

	return render(request,'quizz.html',context)



def QuizzCallBack(request):
	"""!
	@brief Función que procesa las respuestas del juego de quizz
	@param request Peticion http
	"""
	context={}
	context['indicePreguntaActual'] = global_vars.indicePreguntaActual+1
	context['numeroTotalPreguntas'] = len(global_vars.pilaPreguntas)

	boton = global_vars.boton
	global_vars.boton=None

	if boton:
		context['boton'] = boton
		context['tiempoPausa'] = 500
		context['indiceRespuesta'] = global_vars.indiceRespuesta

		if formateaCodigo(boton) == formateaCodigo(str(global_vars.indiceRespuesta)):

			global_vars.indicePreguntaActual+=1
			global_vars.indicadorAciertos+=1

			mensaje=lineaCentrada(1,"Respuesta") + lineaCentrada(2,"Correcta")
			publicarMQTT("Pantalla",mensaje,1)

			context['mensaje'] = "Respuesta correcta"
			#procesar información de respuesta correcta

			context['refrescar'] = True
			music = settings.MEDIA_ROOT + '/songs/correcto.ogg'
			cargarAudios([music])

		else:
			global_vars.indicadorErrores+=1

			mensaje=lineaCentrada(1,"Respuesta") + lineaCentrada(2,"Incorrecta")
			publicarMQTT("Pantalla",mensaje,0)


			context['mensaje'] = "Respuesta incorrecta"
			music = settings.MEDIA_ROOT + '/songs/incorrecto.ogg'
			cargarAudios([music])

	return JsonResponse(context)

#Almacena el mensaje presente en las variables globales

def message(request):
	context = {'glob_message' : global_vars.message,}


# ======== Login zone ========

#Vista para el inicio de sesión de los especialistas

def Login(request):
	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info!',
		'QRM_color' : "QRM_blue",
		'message_text'	:	'Sign in form access to settings.',
	}

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				context['message_alert'] = "alert-success"
				context['message_head'] = "Success! "
				context['message_text'] = "The user <%s> is active." % username
				return HttpResponseRedirect('/settings/')

			else:
				context['message_alert'] = "alert-danger"
				context['message_head'] = "Error, "
				context['message_text'] = "The account-user %s is disable." % username
		else:
			context['message_alert'] = "alert-danger"
			context['message_head'] = "Error, "
			context['message_text'] = "Username or pass incorrects: {0}".format(username)

	return render(request, 'login.html', context)

#Cierra sesion del usuario Especialista o administrador conectado

@login_required
def Logout(request):
    logout(request)
    context = {
		'QRM_color' : "QRM_blue",
    }
    #return render(request, 'home.html', context)
    return HttpResponseRedirect('/')


# ======== Settings zone ========

#Vista de la pantalla principal de las opciones

class Settings(LoginRequiredMixin, TemplateView):
	template_name="settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para la pantalla de creación de actividades, lista y categorias

class Game_settings(LoginRequiredMixin, TemplateView):
	template_name="game_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Game_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para las opciones de los , asociar actividad y terapia y acceder a más opciones de actividad

class Activity_settings(LoginRequiredMixin, TemplateView):
	template_name="activity_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Activity_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista de los Indicadores existentes en el sistema

class Lista_Indicadores(LoginRequiredMixin, ListView):
	model = Actividad
	template_name="indicators_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Lista_Indicadores, self).get_context_data(**kwargs)
		context['Activities'] = Actividad.objects.all
		context['QRM_color'] = "QRM_orange"
		return context


#Vista de las Terapias existentes en el sistema

class Terapia_player_list(LoginRequiredMixin, ListView):
	model = Terapia_Actividad
	template_name="therapy_player_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Terapia_player_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['title'] = "Terapia-Activities"
		context['activities'] = Actividad.objects.all()
		return context

#Vista de los contenidos Multimedia existentes en el sistema

class Gallery(LoginRequiredMixin, ListView):
	model = Multimedia
	template_name="gallery.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Gallery, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting of the gallery."
		context['title'] = "Gallery"
		context['subtitle'] = "Configure your app"
		context['actividad_contenido'] = Actividad_Contenido.objects.all()
		return context

#Vista del detalle de los elementos Multimedia

class Multimedia_detail(LoginRequiredMixin, DetailView):
	model = Multimedia
	template_name = "multimedia_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Multimedia_detail, self).get_context_data(**kwargs)
		if self.object.audio:
			url = str(self.object.audio.url)
		else:  # If there are not file and only exists image:
			url = str(self.object.imagen.url)

		url = url[6:] # Deleting 'files/'

		if not os.path.exists('appQRMusical/files/temp/'):
			os.mkdir('appQRMusical/files/temp/')

		qrencode_command = "qrencode %s -o appQRMusical/files/temp/temp.png -s 6" % (url)
		context['qr'] = os.popen(qrencode_command)

		if context['qr']:
			print("QR code of %s make it!" % self.object.nombre)

		context['QRM_color'] = "QRM_orange"
		context['title'] = "QR code"
		context['subtitle'] = "QR of multimedia %s" % self.object.nombre

		img_thumb = square_thumbnail(self.object.imagen.path)
		imgQR = img_QR("appQRMusical/files/temp/temp.png")
		join_thumbnails(img_thumb, imgQR)

		return context


def square_thumbnail(url):
	thumb_size =300, 300

	img = Image.open(url)
	width, height = img.size

	if width > height:
		delta = width - height
		left = int(delta/2)
		upper = 0
		right = height + left
		lower = height
	else:
		delta = height - width
		left = 0
		upper = int(delta/2)
		right = width
		lower = width + upper

	img = img.crop((left, upper, right, lower))
	img.thumbnail(thumb_size)
	img = img.resize((300,300))
	return img

def img_QR(url):
	imgQR = Image.open(url)
	imgQR = imgQR.resize((300,300))
	imgQR = imgQR.convert('RGB')
	return imgQR


def join_thumbnails(img, imgQR):
	canvas = Image.new('RGB',(600,300))
	canvas.paste(img,(0,0))
	canvas.paste(imgQR,(300,0))
	canvas.save(settings.MEDIA_ROOT+"/temp/img_QR.jpg")

#Vista para la subida de archivos Multimedia a la aplicación

@login_required(login_url='login')
def upload_multimedia(request):

	context = {
		'QRM_color': "QRM_blue",
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info, ',
		'message_text'	:	'Selecciona un fichero y pulsa subir.',
	}

	if request.method == 'POST':
		context['form'] = UploadMultimediaForm(request.POST, request.FILES)
		if context['form'].is_valid():
			file_up = Multimedia()
			files = request.FILES
			data = request.POST
			success_url = '/settings/gallery'
			file_up.imagen = files['imagen']

			if 'file' in files:
				file_up.audio = files['file']
				file_up.name = file_up.audio.name
			else:
				file_up.audio = None
				file_up.name = file_up.imagen.name

			nombre, ext = file_up.name.rsplit('.', 1)
			file_up.nombre = nombre
			file_up.filetype = ext
			file_up.save()

			#if 'players' in dict(request.POST.iterlists()):
			#	file_up.players = dict((request.POST))['players']

			context['message_alert'] = "alert-success"
			context['message_head'] = "Conseguido! "
			context['message_text'] = "Fichero \"%s\" subido con exito, pulse atras para volver a la pantalla anterior " % (file_up.nombre)

	else:
		context['form'] = UploadMultimediaForm()

	return render(request, 'upload.html', context)

#Vista para la actualización de multimedia existente

class Multimedia_update(LoginRequiredMixin, UpdateView):
	model = Multimedia
	form_class = UploadMultimediaForm
	template_name = 'upload.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse_lazy('multimedia_update', kwargs={'pk': self.object.id_contenido})

#Vista para la eliminacion de multimedia existente

class Multimedia_delete(DeleteView):
	model = Multimedia
	success_url = '/settings/gallery'
	def get_object(self):
		obj = super(Multimedia_delete, self).get_object()

		if obj.audio:
			path_file = join_url_with_media_root(obj.audio.url)
			os.remove(path_file)

		path_image = join_url_with_media_root(obj.image.url)
		os.remove(path_image)
		return obj


def join_url_with_media_root(url):
	url = url[6:] # del 'files/'....
	path = os.path.join(settings.MEDIA_ROOT+'%s' % url)
	return path

#Vista de las Actividades existentes en el sistema

class Actividads_list(LoginRequiredMixin, ListView):
	model = Actividad
	template_name="players_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Actividads_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['categoria'] = Categoria_Actividad.objects.all()
		return context

#Vista de loss Usuarios existentes en el sistema

class Users_list(LoginRequiredMixin, ListView):
	model = Paciente
	template_name="users_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Users_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['title'] = "Users"
		nacimiento = Paciente.objects.all()#Calculamos la edad de los pacientes
		for i in nacimiento:
			if i.edad == None:
				i.edad = (date.today().year - i.fecha_de_nacimiento.year - ((date.today().month, date.today().day) < (i.fecha_de_nacimiento.month, i.fecha_de_nacimiento.day)))
				i.save()
		return context

#Vista de los Tratamientos existentes en el sistema

def Tratamientos_list(request):
	model = Tratamiento
	req = request.user.id
	thera = Especialista.objects.get(user_id=req)
	sup = Supervisa.objects.filter(especialista_id=thera)
	#for i in sup:
		#sup1 = sup.objects.get(id=i)
		#wanted_id = sup.treatment_id
	#treatments = Tratamiento.objects.filter(id=sup.treatment.id)
	template_name="treatments_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'object_list' : Tratamiento.objects.all(),
	'thera' : thera,
    'supervise' :  Supervisa.objects.all()
	}
	return render(request,'treatments_list.html',context)

#Vista de las Terapias existentes en el sistema

def Therapies_list(request):
	req = request.user.id
	thera = Especialista.objects.get(user_id=req)
	asig_t = Especialista_Asigna_Terapia.objects.filter(especialista_id=thera)
	template_name="therapies_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'object_list' : Terapia.objects.all(),
	'asign_therapy' : Especialista_Asigna_Terapia.objects.all(),
    'asign' : asig_t
	}
	return render(request,'therapies_list.html',context)

#Vista del resumen general de las relaciones dentro del sistema

def Summary(request):

	template_name="treatments_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'patients' : Paciente.objects.all(),
	'treatments' : Tratamiento.objects.all(),
	'therapies' : Asigna_Terapia.objects.all(),
	'activities' : Terapia_Actividad.objects.all()
	}
	return render(request,'summary.html',context)

#Vista de los Especialistas existentes en el sistema

@login_required(login_url='login')
def Especialistas_list(request):
	template_name="therapists_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color': "QRM_orange",
		'thera_list' : Especialista.objects.all(),
		'admin' : request.user.is_staff
	}
	return render(request,'therapists_list.html',context)

#Vista para crear Especialistas en el sistema

class Create_therapist(LoginRequiredMixin, CreateView):
	model = Paciente
	form_class = FormularioEspecialista
	template_name="create_therapist.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapists_list')

	def get_context_data(self, **kwargs):
		context = super(Create_therapist, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Create Player"
		context['subtitle'] = "Create your player"
		context['btn_label'] = "Create"
		return context

#Vista de los Pacientes existentes en el sistema

class Create_user(LoginRequiredMixin, CreateView):
	model = Paciente
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Create_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para actualizar los Pacientes del sistema

class Update_user(LoginRequiredMixin, UpdateView):
	model = Paciente
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['image'] = Paciente.objects.get(id=self.object.id)
		context['user_id'] = self.object.id
		return context

#Vista para eliminar Pacientes del sistema

class User_delete(DeleteView):
	model = Paciente
	success_url = '/settings/users_list/'
	def get_object(self):
		obj = super(User_delete, self).get_object()
		return obj

#Vista para eliminar las terapias asociadas con actividades en el sistema

class Delete_therapy_player(DeleteView):
	model = Terapia_Actividad
	success_url = '/settings/Activities/therapy-player/'
	def get_object(self):
		obj = super(Delete_therapy_player, self).get_object()
		return obj

#Vista para eliminar  del sistema la tarjeta asociada con un jugador

def ID_delete(request, pk):
    model = get_object_or_404(Paciente, pk=pk)
    model.codigo = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Informacion actualizada.",
        'title' : "Actualiza los Ususarios",
        'subtitle' : "Actualiza y configura tu usuario",
        'btn_label' : 'Actualiza',
        'source' : '/files/static/success.png'
        }
    return render(request,'user_ID.html',context)

#Vista para asociar del sistema la tarjeta asociada con un jugador

def User_ID(request, pk):
    model = get_object_or_404(Paciente, pk=pk)
    users = Paciente.objects.all()
    cards = Multimedia.objects.all()
    #code = Identify_ID()
    code = global_vars.boton_mqtt
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "La información se ha actualizado correctamente.",
        'title' : "Info",
        'subtitle' : "TERMINADO CON EXITO!!",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    for i in users:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO, PRUEBE UNO NUEVO",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)

    for i in cards:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN ARCHIVO MULTIMEDIA, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)

    model.codigo = code
    model.save()
    return render(request,'user_ID.html',context)

#Vista que elimina un tarjeta con su elemento multimedia

def Multi_ID_delete(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    model.codigo = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Informacion actualizada.",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    return render(request,'card_ID.html',context)

#Vista que vincula un tarjeta con su elemento multimedia

def Multi_ID(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    users = Paciente.objects.all()
    cards = Multimedia.objects.all()
    #code = Identify_ID()
    code=global_vars.boton_mqtt
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "La información se ha actualizado correctamente.",
        'title' : "Info View",
        'subtitle' : "TASK DONE!!",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    for i in cards:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN ARCHIVO MULTIMEDIA, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'card_ID.html',context)

    for i in users:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN USUARIO, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'card_ID.html',context)

    model.codigo = code
    model.save()
    return render(request,'card_ID.html',context)

#Vista que vincula una Categoría con una Actividad

class Add_category_player(LoginRequiredMixin, CreateView):
	model = Categoria_Actividad
	form_class = FormularioCategoriaActividad
	template_name="playerc_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Add_category_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que vincula una Terapia con una Actividad

class Add_therapy_player(LoginRequiredMixin, CreateView):
	model = Terapia_Actividad
	form_class = UploadTherapyFormActividad
	template_name="therapy_player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapy_player')

	def get_context_data(self, **kwargs):
		context = super(Add_therapy_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que crea una Actividad

def Create_player(request):
	context = {
		'QRM_color'		: "QRM_blue"
	}
	if request.method == 'POST':
		context['form'] = FormularioActividad(request.POST)
		context['form1'] = UploadIndicatorForm(request.POST)
		context['form2'] = UploadOnePlayerTerapiaForm(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid() & context['form2'].is_valid():
#			indi = Player_Indicator()
			act = Actividad()
			TA = Terapia_Actividad()
			act = context['form'].save(commit=False)
			act = context['form1'].save(commit=False)
			TA = context['form2'].save(commit=False)
			act.nombre = context['form'].cleaned_data['nombre']
			act.descripcion = context['form'].cleaned_data['descripcion']
			act.proposito = context['form'].cleaned_data['proposito']
			act.save()
			indi = context['form1'].cleaned_data['indicador']
			terapia = context['form2'].cleaned_data['terapia']

			print(terapia)
			asigna_indi = Indicador.objects.filter(pk__in=indi)
			#asigna_tera = Terapia.objects.filter(pk__in=terapia)
			print(asigna_indi)
			if indi:
				for i in asigna_indi:
					act.indicador.add(i)
			if terapia:
				TA.actividad = act
				TA.terapia = terapia
				TA.save()
			context['object_list'] = Actividad.objects.all()
			return render(request, 'players_list.html', context)
	else:
		context['form'] = FormularioActividad()
		context['form1'] = UploadIndicatorForm()
		context['form2'] = UploadOnePlayerTerapiaForm ()
	return render(request, 'create_player.html', context)

#Vista que actualiza una Actividad

class Update_player(LoginRequiredMixin, UpdateView):
	model = Actividad
	form_class = FormularioActividad
	template_name="player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Update_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['therapy'] = Terapia_Actividad.objects.filter(actividad_id=self.object.id)
		context['indicators'] = Indicador.objects.all()
		#context['playerindicators'] = Actividad_Indicador.objects.filter(player_id=self.object.id)
		context['activities'] = Actividad_Contenido.objects.filter(actividad_id=self.object.id)
		context['player_id'] = self.object.id
		return context


#Vista que elimina una Actividad

class Actividad_delete(DeleteView):
	model = Actividad
	success_url = '/settings/players_list/'
	def get_object(self):
		obj = super(Actividad_delete, self).get_object()
		return obj

#Vista que crea un Indicador

class Create_indicator(LoginRequiredMixin, CreateView):
	model = Actividad
	form_class = UploadIndicatorForm
	template_name="indicator_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('indicators_list')

	def get_context_data(self, **kwargs):
		context = super(Create_indicator, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que actualiza un Indicador

class Update_indicator(LoginRequiredMixin, UpdateView):
	model = Actividad
	form_class = UploadIndicatorForm
	template_name = 'indicator_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse_lazy('indicators_list')

#Vista que elimina un Indicador

class Indicador_delete(DeleteView):
	model = Indicador
	success_url = '/settings/activities/indicators'
	def get_object(self):
		obj = super(Indicador_delete, self).get_object()
		return obj


class Multimedia_delete(DeleteView):
	model = Multimedia
	success_url = '/settings/gallery'
	def get_object(self):
		obj = super(Multimedia_delete, self).get_object()

		if obj.audio:
			path_file = join_url_with_media_root(obj.audio.url)
			os.remove(path_file)

		path_image = join_url_with_media_root(obj.image.url)
		os.remove(path_image)
		return obj

#Vista que crea un Tratamiento

def Create_treatment(request):
	context = {
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Tratamiento.',
		'QRM_color'	: "QRM_blue"
	}

	if request.method == 'POST':
		context['form'] = UploadTreatmentForm(request.POST)
		context['form1'] = UploadAsignTherapyForm(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid():
			supervise = Supervisa()
			asigna = Asigna_Terapia()
			req = request.user.id
			thera = Especialista.objects.get(user_id=req)
			Tratamiento = context['form'].save(commit=False)
#			Asigna_Terapia = context['form1'].save(commit=False)
			terapia = context['form1'].cleaned_data['terapia']
			#print(terapia)
			asigna_list = Terapia.objects.filter(pk__in=terapia)
			Tratamiento.paciente = context['form'].cleaned_data['paciente']
			Tratamiento.nombre = context['form'].cleaned_data['nombre']
			Tratamiento.fecha_inicio = context['form'].cleaned_data['fecha_inicio']
			Tratamiento.fecha_fin = context['form'].cleaned_data['fecha_fin']
			Tratamiento.descripcion = context['form'].cleaned_data['descripcion']
			Tratamiento.activado = context['form'].cleaned_data['activado']
			Tratamiento.save()
			supervise.tratamiento = Tratamiento
			supervise.especialista = thera
			supervise.save()
			if terapia:
				asigna.tratamiento = Tratamiento
				asigna.save()
				for i in asigna_list:
					asigna.terapia.add(i)
					#asigna.terapia = i
					#asigna.save()
			return render(request, 'settings.html', context)

	else:
		context['form'] = UploadTreatmentForm()
		context['form1'] = UploadAsignTherapyForm()
	return render(request, 'treatment_details.html', context)

#Vista que actualiza un Tratamiento

class Update_treatment(LoginRequiredMixin, UpdateView):
	model = Tratamiento
	form_class = UploadTreatmentForm
	template_name="treatment_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('treatments_list')

	def get_context_data(self, **kwargs):
		context = super(Update_treatment, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina un Tratamiento

class Tratamiento_delete(DeleteView):
	model = Tratamiento
	success_url = '/settings/treatments_list/'
	def get_object(self):
		obj = super(Tratamiento_delete, self).get_object()
		return obj

#Vista que crea una Terapia

def Create_therapy(request):

	context = {
		'QRM_color'	: "QRM_blue"
	}

	if request.method == 'POST':
		context['form'] = UploadTherapyForm(request.POST)
		context['form1'] = UploadOneActividadTherapyForm(request.POST)
		context['form2'] = UploadAsign(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid() & context['form2'].is_valid():
			TAT = Especialista_Asigna_Terapia()
			req = request.user.id
			tera = Terapia()
			thera = Especialista.objects.get(user_id=req)
			tera = context['form'].save(commit=False)
			Terapia_Actividad = context['form1'].save(commit=False)
			Asigna_Terapia = context['form2'].save(commit=False)
			tera.paciente = context['form'].cleaned_data['nombre']
			tera.description = context['form'].cleaned_data['descripcion']
			tera.tipo = context['form'].cleaned_data['tipo']
			tera.save()
			Terapia_Actividad.terapia = tera
			Terapia_Actividad.actividad = context['form1'].cleaned_data['actividad']
			tratamiento = context['form2'].cleaned_data['tratamiento']
			print(Terapia_Actividad.terapia)
			if tratamiento:
				Asigna_Terapia.tratamiento = tratamiento
				Asigna_Terapia.save()
				Asigna_Terapia.terapia.add(tera)
				TAT.asigna_terapia = Asigna_Terapia
				TAT.especialista = thera
				print(TAT)
				TAT.save()
			try:
				Terapia_Actividad.actividad
				Terapia_Actividad.save()
			except:
				context['message_alert'] = 'alert-success'
				context['message_head'] = 'Success!!. '
				context['message_text'] = 'Changes saved successfully'

			context['object_list'] = Terapia.objects.all()
			context['asign_therapy'] = Especialista_Asigna_Terapia.objects.all()
			return render(request, 'therapies_list.html', context)
	else:
		context['form'] = UploadTherapyForm()
		context['form1'] = UploadOneActividadTherapyForm()
		context['form2'] = UploadAsign()
	return render(request, 'therapy_details.html', context)

#Vista que actualiza una Terapia

class Update_therapy(LoginRequiredMixin, UpdateView):
	model = Terapia
	form_class = UploadTherapyForm
	template_name="therapy_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapies_list')

	def get_context_data(self, **kwargs):
		context = super(Update_therapy, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina una Terapia

class Terapia_delete(DeleteView):
	model = Terapia
	success_url = '/settings/therapies_list/'
	def get_object(self):
		obj = super(Terapia_delete, self).get_object()
		return obj

#Vista que muestra la lista de Categorias presentes en el sistema

class Categories_list(LoginRequiredMixin, ListView):
	model = Categoria
	template_name="categories_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Categories_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Actual list of categories."
		context['title'] = "Categories"
		context['subtitle'] = "Configure your app"
		return context

#Vista que crea una Categoría

class Create_category(LoginRequiredMixin, CreateView):
	model = Categoria
	form_class = UploadCategoryForm
	template_name="category_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('categories_list')

	def get_context_data(self, **kwargs):
		context = super(Create_category, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Creating a category."
		context['title'] = "Create a category"
		context['subtitle'] = "Create your Categories"
		context['btn_label'] = "Create"
		return context

#Vista que actualiza una Categoría

class Update_category(LoginRequiredMixin, UpdateView):
	model = Categoria
	form_class = UploadCategoryForm
	template_name = 'category_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse_lazy('categories_list')

#Vista que elimina una Categoría

class Categoria_delete(DeleteView):
	model = Categoria
	success_url = '/settings/Categories'
	def get_object(self):
		obj = super(Categoria_delete, self).get_object()
		return obj

#Vista que muestra la lista de Diagnósticos presentes en el sistema

def Diagnostico_list(request, pk):
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color' : "QRM_orange",
		'ide' : pk,
		'object_list' : Diagnostico.objects.filter(paciente_id=pk),
	}
	return render(request, 'diagnostic_list.html', context)

#Vista que crea un Diagnóstico

@login_required(login_url='login')
def Create_diagnostic(request, pk):
	context = {
		'QRM_color' :"QRM_blue",
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Tratamiento.'
	}
	profile = Paciente.objects.get(id=pk)

	if request.method == 'POST':
		context['form'] = UploadDiagnosticForm(request.POST)
		if context['form'].is_valid():
			diagnostic = Diagnostico()
			diagnostic.paciente = profile
			diagnostic.valoracion = context['form'].cleaned_data['valoracion']
			diagnostic.notas = context['form'].cleaned_data['notas']
			diagnostic.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['object_list'] = Diagnostico.objects.filter(paciente_id=pk)
			return render(request, 'diagnostic_list.html', context)
	else:
		context['form'] = UploadDiagnosticForm()
	return render(request, 'diagnostic.html', context)

#Vista que actualiza un Diagnóstico

class Update_diagnostic(LoginRequiredMixin, UpdateView):
	model = Diagnostico
	form_class = UploadDiagnosticForm
	template_name="diagnostic.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_diagnostic, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina un Diagnóstico

class Delete_diagnostic(DeleteView):
	model = Diagnostico
	success_url = reverse_lazy('users_list')
	def get_object(self):
		obj = super(Delete_diagnostic, self).get_object()
		return obj

#Vista que muestra el contenido disponible para vincular con la actividad

@login_required(login_url='login')
def add_multimedia_to_player(request, id):
	objs = Actividad.objects.filter(id=id)
	listcont = Actividad_Contenido.objects.filter(actividad_id=id)
	content = Contenido.objects.all()
	content1 = list(content)
	for obj in content:
		for i in listcont:
			if i.contenido.id_contenido == obj.id_contenido:
				content1.remove(obj)
	context = {
		'object_list' 	:content1,
		'object_list1' 	:listcont,
		'title' 		: objs[0],
		'activities'    : objs,
		'subtitle'		: "Add Contenido to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id
		}

	return render(request, 'add_multimedia_to_player.html', context)

#Vista que vincula el contenido seleccionado con una actividad

@login_required(login_url='login')
def add_multimedia_to_player_function(request, id_player, id_multimedia):
	player_to_add = Actividad.objects.get(id=id_player)
	mults = Contenido.objects.get(id_contenido=id_multimedia)
	new_content = Actividad_Contenido()
	new_content.actividad = player_to_add
	new_content.contenido = mults
	new_content.save()

	objs = Actividad.objects.filter(id=id_player)

	context = {
		'object_list' 	: Actividad_Contenido.objects.exclude(actividad_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add Contenido to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id_player
		}
	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)

#Vista que elimina el contenido asociado con una actividad

@login_required(login_url='login')
def del_multimedia_of_player_function(request, id_player, id_multimedia):
	player_to_del = Actividad.objects.get(id=id_player)
	mults = Actividad_Contenido.objects.filter(contenido_id=id_multimedia)
	mults = mults.get(actividad_id=id_player)
	mults.delete()

	objs = Actividad.objects.filter(id=id_player)

	context = {
		'object_list' 	:Actividad_Contenido.objects.exclude(actividad_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		}

	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)

#Vista que muestra las opciones del especialista (cambiar nombre,apellido, contraseña o email)

class User(LoginRequiredMixin, TemplateView):
	template_name="user.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('user')
	def get_context_data(self, **kwargs):
		context = super(User, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que muestra la lista de pacientes para seleccionar y ver sus Resultados

class Resultados(LoginRequiredMixin, ListView):
	template_name="results.html"
	model = Paciente
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('settings')
	def get_context_data(self, **kwargs):
		context = super(Resultados , self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que muestra la lista de las tratamiento para el paciente seleccionado y ver sus Resultados

def ResultadosTratamiento(request, pk):
	objects = Tratamiento.objects.filter(paciente__id=pk)
	context = {
		'QRM_color' : "QRM_orange",
		'objects' : objects,
		'paciente' : Paciente.objects.get(pk=pk)
	}
	return render(request, 'results_treatment.html', context)

#Vista que muestra la lista de Resultados para el tratamiento especificada

def Resultados_details(request, pk):

	objects_treat = Tratamiento.objects.filter(id=pk)
	objects = Resultado_Sesion.objects.filter(sesion_id__in=Sesion.objects.filter(asigna_Terapia__tratamiento__in=objects_treat))
	success = objects.filter(indicador_id=5)
	fail = objects.filter(indicador_id=4)
	timing = objects.filter(indicador_id=6)
	print(success)
	print(fail)
	print(timing)
	context = {
		'QRM_color' : "QRM_orange",
		'message_alert' : "alert-info",
		'message_head' : "Info, ",
		'message_text' : "Resultado table.",
		'title' : "Resultados",
		'success' : success,
		'failures' : fail,
		'time' : timing,
		#'data' : data,
		'objects_treat' : objects_treat,
		'objects' : objects,
		'subtitle' : "Add the data that you want"
	}
	return render(request, 'results_details.html', context)

#Vista para cambiar el Nombre y el Apellido del especialista

@login_required(login_url='login')
def edit_name(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}

	if request.method == 'POST':
		context['form'] = EditNameForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Especialista.objects.get(user_id=req)
			request.user.first_name = context['form'].cleaned_data['name']
			request.user.last_name = context['form'].cleaned_data['surname']
			therapist.nombre = context['form'].cleaned_data['name']
			therapist.apellido = context['form'].cleaned_data['surname']
			request.user.save()
			therapist.save()
			context['QRM_color'] ="QRM_blue"
			context['thera_list'] = Especialista.objects.all()
			context['admin'] = request.user.is_staff
			return render(request, 'therapists_list.html', context)
	else:
		context['form'] = EditNameForm(
		request=request,
		initial={'name': request.user.first_name,'surname': request.user.last_name})
	return render(request, 'userForms.html', context)

#Vista para cambiar el Email del especialista

@login_required(login_url='login')
def edit_email(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}

	if request.method == 'POST':
		context['form'] = EditEmailForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Especialista.objects.get(user_id=req)
			request.user.email = context['form'].cleaned_data['email']
			therapist.email = context['form'].cleaned_data['email']
			request.user.save()
			therapist.save()
			context['QRM_color'] ="QRM_blue"
			context['thera_list'] = Especialista.objects.all()
			context['admin'] = request.user.is_staff
			return render(request, 'therapists_list.html', context)
	else:
		context['form'] = EditEmailForm(
		request=request,
		initial={'email': request.user.email})
	return render(request, 'userForms.html', context)

#Vista para cambiar la Contraseña del especialista

@login_required(login_url='login')
def edit_password(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}

	if request.method == 'POST':
		context['form'] = EditPassForm(request.POST)
		if context['form'].is_valid():
			request.user.password = make_password(context['form'].cleaned_data['password'])
			request.user.save()
	else:
		context['form'] = EditPassForm()
	return render(request, 'userForms.html', context)
