"""!
@package models.py
@brief Archivo de models
@author Gregorio Corpas Prieto
@date 13/03/2019
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

Valores_Online = [
    ("si", "si"),
    ("no", "no"),
]
Genero = [
    ("Masculino","Masculino"),
    ("Femenino","Femenino"),
]
Nivel = [
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
]
Juego = [
    ("Matching","Matching"),
    ("Quiz","Quiz"),
    ("Evoca","Evoca"),
]
Formato = [
    ("Texto","Texto"),
    ("Imagen","Imagen"),
    ("Audio","Audio"),
    ("Video","Video"),
]

Visualizacion= [
    ("Multiopcion","Multiopcion"),
    ("Unica","Unica"),
]

Resultado = [
    ("True","True"),
    ("False","False"),
    ("",""),
]

def generarDirectorioSubida(self, file):
    """!
    @brief Función que anexa al archivo pasado por parámetro el directorio en el que debe ser colocado
    @param self Llamada al propio método
    @param file Archivo de caracter multimedia
    """
    nombre, extension = os.path.splitext(file)
    extension.lower()
    directory = ''

    if extension == '.jpg' or extension == '.jpeg':
        directory = 'images/'

    if extension == '.mp3' or extension == '.wav':
        directory = 'songs/'

    if extension == '.mp4' or extension == '.wmv' or extension == '.mpg' or extension == '.avi':
        directory = 'movies/'

    return os.path.join(directory, file)

def calcularEdad(self,fecha_de_nacimiento):
    """!
    @brief Función que calcula la edad a partir de una fecha dada
    @param self Llamada al propio método
    @param fecha_de_nacimiento Fecha a partir la cuál calcular la edad
    """
    hoy = date.today()
    return hoy.year - fecha_de_nacimiento.year - ((hoy.month, hoy.day) < (fecha_de_nacimiento.month, fecha_de_nacimiento.day))

@receiver(post_save, sender=User)
def create_therapist_profile(sender, instance, created, **kwargs):
    if created:
        Especialista.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_therapist_profile(sender, instance, **kwargs):
    instance.especialista.save()

class Indicador(models.Model):
    """!
    @brief Clase que define el Indicador para medición de métricas de juego
    """
    ##Identificador de tupla
    id =  models.AutoField(primary_key=True)
    ##Nombre del Indicador
    nombre = models.CharField(max_length=50, blank=True)
    ##Descripción del Indicador
    descripcion = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Indicador"
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    """!
    @brief Clase que define la Actividad o juego
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Nombre de Actividad
    nombre = models.CharField(max_length=100)
    ##Descripción de Actividad
    descripcion = models.CharField(max_length=200, blank=True)
    ##Propósito de Actividad
    proposito = models.CharField(max_length=100, blank=True)
    ##Indicadores de métricas asociados a la Actividad
    indicador = models.ManyToManyField(Indicador, blank=True)
    ##Tipo de juego
    juego = models.CharField(max_length=20, choices=Juego, default="Matching")
    ##Flag para indicar si las preguntas seguirán el orden de creación o se mostrarán de modo aleatorio
    aleatorio = models.BooleanField(default=False)
    ##Flag para determinar si las preguntas serán narradas
    narracion = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Actividad"
    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    """!
    @brief Clase que define el Paciente o jugador
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Imagen de perfil
    imagen = models.ImageField(upload_to='profiles/', blank=True)
    ##Nombre del Paciente
    nombre = models.CharField("Nombre",max_length=50)
    ##Apellidos del Paciente
    apellido = models.CharField("Apellido",max_length=50)
    ##Fecha de nacimiento del Paciente
    fecha_de_nacimiento = models.DateField(null=True,blank=True)
    ##Edad del Paciente
    edad = models.IntegerField(null=True,blank=True)
    ##Género del paciente
    genero = models.CharField(max_length=10,choices = Genero, blank=True)
    ##Nivel a determinar
    nivel = models.IntegerField(choices = Nivel,default=1)
    ##Código de pulsera RFID para login
    codigo = models.CharField(max_length=8, blank=True)
    ##Flag para determinar estado online
    online = models.CharField(max_length=10, choices=Valores_Online, default="no")
    class Meta:
        verbose_name_plural = "Paciente"
    def __str__(self):
        return self.nombre

class Especialista(models.Model):
    """!
    @brief Clase que define el Especialista administrador
    """
    ##Nombre de Usuario Especialista
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ##Nombre del especialista
    nombre = models.CharField("Nombre",max_length=50)
    ##Apellidos del especialista
    apellido = models.CharField("Apellido",max_length=50)
    ##Correo electrónico del especialista
    email = models.EmailField()
    class Meta:
        verbose_name_plural = "Especialista"

class Tratamiento(models.Model):
    """!
    @brief Clase que define el Tratamiento que se aplicará a los pacientes
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Nombre de Tratamiento
    nombre = models.CharField("Nombre",max_length=50)
    ##Paciente a tratar
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    ##Fecha de inicio del tratamiento
    fecha_inicio = models.DateField(null=True,blank=True)
    ##Fecha de finalización del tratamiento
    fecha_fin = models.DateField(null=True,blank=True)
    ##Descripción del tratamiento
    descripcion = models.TextField(blank=True)
    ##Flag para determinar si está activo el tratamiento
    activado = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Tratamiento"
    def __str__(self):
        return self.nombre

class Terapia(models.Model):
    """!
    @brief Clase que define la Terapia que engloba Actividades y que a su vez conforma un Tratamiento
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Nombre de Terapia
    nombre = models.CharField("Nombre",max_length=50)
    ##Descripción de la Terapia
    descripcion = models.TextField(blank=True)
    ##Tipo de Terapia
    tipo = models.CharField("Tipo",max_length=50)
    class Meta:
        verbose_name_plural = "Terapia"
    def __str__(self):
        return self.nombre

class Terapia_Tratamiento(models.Model):
    """!
    @brief Clase que relaciona las distintas Terapias con los Tratamientos
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Terapia a relacionar
    terapia = models.ManyToManyField(Terapia)
    ##Tratamiento a relacionar
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Terapia_Tratamiento"
    def __str__(self):
        return "{}:{}".format(self.terapia,self.tratamiento)
    def getNombre(id):
        return Terapia.objects.filter(id=id)

class Especialista_Terapia_Tratamiento(models.Model):
    """!
    @brief Clase que relaciona los Especialistas con los Tratamientos y las respectivas Terapias que los componen
    """
    ##Tupla terapia_tratamiento involucrada
    terapia_tratamiento = models.ForeignKey(Terapia_Tratamiento,on_delete=models.CASCADE)
    ##Especialista asignado
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    ##Fecha de la asignación
    fecha = models.DateField(null=True,blank=True)
    class Meta:
        verbose_name_plural = "Especialista_Terapia_Tratamiento"
        unique_together = ("terapia_tratamiento","especialista","fecha")

class Supervisa(models.Model):
    """!
    @brief Clase que relaciona los Tratamientos con los Especialistas que los supervisan
    """
    ##Especialista a relacionar
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    ##Tratamiento a relacionar
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Supervisa"
        unique_together = ("especialista","tratamiento")

class Diagnostico(models.Model):
    """!
    @brief Clase que define el Diagnóstico que se realiza a un Paciente
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Paciente involucrado
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    ##Fecha
    fecha = datetime.today()
    ##Valoración del Especialista
    valoracion = models.CharField(max_length=50, blank=True)
    ##Campo para anotaciones
    notas = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Diagnostico"

class Sesion(models.Model):
    """!
    @brief Clase que define la Sesión de trabajo en una Actividad
    """
    ##Identificador de tupla
    id = models.AutoField(primary_key=True)
    ##Tupla de relación terapia_tratamiento
    terapia_tratamiento = models.ForeignKey(Terapia_Tratamiento,on_delete=models.CASCADE)
    ##Actividad involucrada
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    ##Instante de inserción
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Sesion"
    def __str__(self):
        return "{}:{}".format(self.terapia_tratamiento,self.fecha.strftime("%b-%d-%Y %H:%M:%S"))

class Terapia_Actividad(models.Model):
    """!
    @brief Clase que relaciona la Terapia con las Actividades que la conforman
    """
    ##Actividad a relacionar
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    ##Terapia a relacionar
    terapia = models.ForeignKey(Terapia,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Terapia_Actividad"
        unique_together = ("actividad","terapia")

class Resultado_Sesion(models.Model):
    """!
    @brief Clase que relaciona las Sesiones de Actividad con los resultados obtenidos por los Indicadores
    """
    ##Sesión de actividad
    sesion = models.ForeignKey(Sesion,on_delete=models.CASCADE)
    ##Indicador a almacenar
    indicador = models.ForeignKey(Indicador,on_delete=models.CASCADE)
    ##Actividad involucrada
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    ##Valor resultado
    resultado =  models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Resultado_Sesion"
        unique_together = ("sesion","indicador","actividad")

class Categoria(models.Model):
    """!
    @brief Clase que define Categoria con la que etiquetar Actividades
    """
    ##Identificador de tupla
    id =  models.AutoField(primary_key=True)
    ##Nombre de la categoría
    nombre = models.CharField(max_length=50, blank=True)
    class Meta:
        verbose_name_plural = "Categoria"
    def __str__(self):
        return self.nombre

class Categoria_Actividad(models.Model):
    """!
    @brief Clase que relaciona la Actividad con Categoria
    """
    ##Categoría a relacionar
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    ##Actividad a relacionar
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categoria_Actividad"
        unique_together = ("categoria","actividad")

class Contenido(models.Model):
    """!
    @brief Clase que define la unidad mínima de Contenido
    """
    ##Identificador de tupla
    id =  models.AutoField(primary_key=True)
    ##Descripción del contenido
    descripcion =  models.CharField(max_length=50, blank=True)
    ##Código RFID asociado al contenido
    codigo = models.CharField(max_length=8, blank=True)
    class Meta:
        verbose_name_plural = "Contenido"
    def __str__(self):
        return self.descripcion

class Multimedia(Contenido):
    """!
    @brief Clase que define un objeto Multimedia
    @param Contenido Es la clase a la cuál extendemos añadiendo más campos
    """
    ##Nombre del objeto multimedia
    nombre = models.CharField(max_length=100)
    ##Objeto de audio
    audio = models.FileField(upload_to=generarDirectorioSubida, null=True, blank=True)
    ##Objeto de video
    video = models.FileField(upload_to=generarDirectorioSubida, null=True, blank=True)
    ##Objeto de imagen
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    ##Instante de inserción
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Multimedia"
        ordering = ('datetime',)

    def __str__(self):
        return self.nombre

    """!
    @brief Clase que relaciona Actividad con Contenido (Deprecated)
    """
class Actividad_Contenido(models.Model):
    ##Actividad a relacionar
    actividad= models.ForeignKey(Actividad,on_delete=models.CASCADE)
    ##Contenido a relacionar
    contenido = models.ForeignKey(Contenido,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Actividad_Contenido"
        unique_together = ("actividad","contenido")


class Pregunta(models.Model):
    """!
    @brief Clase que define un objeto Pregunta básico para componer la Actividad
    """
    ##Texto que conforma la pregunta
    pregunta = models.TextField(blank=False,null=False)
    ##Tipo de multimedia que dan formato a la pregunta
    formato = models.CharField(max_length=20, choices=Formato, default="Imagen")
    class Meta:
        verbose_name_plural = "Pregunta"
    def __str__(self):
        return self.pregunta

class Pregunta_Matching(Pregunta):
    """!
    @brief Clase que define un objeto Pregunta_Matching
    @param Contenido Es la clase a la cuál extendemos añadiendo más campos
    """
    ##Multimedia asociado a la pregunta
    multimediaPregunta = models.ForeignKey("Multimedia",related_name="multimedia+",blank=True, null=True,on_delete=models.CASCADE)
    ##Respuesta
    respuesta = models.ForeignKey("Respuesta",related_name="respuesta+",blank=False,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Pregunta_Matching"
    def __str__(self):
        return "{} : {}".format(self.pregunta,self.respuesta)

class Pregunta_Quiz(Pregunta):
    """!
    @brief Clase que define un objeto Pregunta_Quiz
    @param Contenido Es la clase a la cuál extendemos añadiendo más campos
    """
    ##Multimedia asociado a la pregunta
    multimediaPregunta = models.ForeignKey("Multimedia",related_name="pregunta+",blank=True, null=True,on_delete=models.CASCADE)
    ##Posibles respuestas
    respuestas = models.ManyToManyField("Respuesta",related_name="respuestas+",blank=False)
    ##Modo de visualización
    visualizacion = models.CharField(max_length=20, choices=Visualizacion, default="Unica")
    class Meta:
        verbose_name_plural = "Pregunta_Quiz"
    def __str__(self):
        return "{}".format(self.pregunta)

class Actividad_Pregunta(models.Model):
    """!
    @brief Clase que relaciona una Actividad con la Pregunta que la componen
    """
    ##Identificador para tupla
    id =  models.AutoField(primary_key=True)
    ##Actividad a relacionar
    actividad= models.ForeignKey(Actividad,on_delete=models.CASCADE)
    ##Pregunta a relacionar
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("actividad","pregunta")
        verbose_name_plural = "Actividad_Pregunta"

class Respuesta(models.Model):
    """!
    @brief Clase que define un objeto Respuesta para asignar a la Pregunta
    """
    ##Objeto multimedia asociado a la respuesta
    multimedia = models.ForeignKey("Multimedia",related_name="multimedia",blank=False,on_delete=models.CASCADE)
    ##Resultado posible para esta respuesta
    resultado =  models.CharField(max_length=20, choices=Resultado, default=None,blank=True)
    class Meta:
        verbose_name_plural = "Respuesta"
    def __str__(self):
        return "{} : {}".format(self.multimedia,self.resultado)

class Registro_Sesion(models.Model):
    """!
    @brief Clase que define un objeto Registro_Sesion donde se guarda cada acción realizada en una Actividad para cada Respuesta a cada Pregunta
    """
    ##Identificador para tupla
    id = models.AutoField(primary_key=True)
    ##Sesion a la que pertenece este registro
    sesion = models.ForeignKey("Sesion",related_name="sesion+",blank=False,on_delete=models.CASCADE)
    ##Pregunta a la que pertenece este registro
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    ##Objeto multimedia utilizado como respuesta
    multimediaRespuesta = models.ForeignKey("Multimedia",related_name="multimediaRespuesta+",null=True,blank=True,on_delete=models.CASCADE)
    ##Instante en el que se respondió
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Registro_Sesion"
    def __str__(self):
        return "{}:{}:{}".format(self.sesion,self.pregunta,self.fecha)
