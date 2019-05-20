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
    ("Quizz","Quizz"),
    ("Calculo","Calculo"),
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
    id =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Indicador"
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    proposito = models.CharField(max_length=100, blank=True)
    indicador = models.ManyToManyField(Indicador, blank=True)
    juego = models.CharField(max_length=20, choices=Juego, default="Matching")
    aleatorio = models.BooleanField(default=False)
    narracion = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Actividad"
    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='profiles/', blank=True)
    nombre = models.CharField("Nombre",max_length=50)
    apellido = models.CharField("Apellido",max_length=50)
    fecha_de_nacimiento = models.DateField(null=True,blank=True)
    edad = models.IntegerField(null=True,blank=True)
    genero = models.CharField(max_length=10,choices = Genero, blank=True)
    nivel = models.IntegerField(choices = Nivel,default=1)
    codigo = models.CharField(max_length=8, blank=True)
    online = models.CharField(max_length=10, choices=Valores_Online, default="no")
    class Meta:
        verbose_name_plural = "Paciente"
    def __str__(self):
        return self.nombre

class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre",max_length=50)
    apellido = models.CharField("Apellido",max_length=50)
    email = models.EmailField()
    class Meta:
        verbose_name_plural = "Especialista"

class Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=50)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True,blank=True)
    fecha_fin = models.DateField(null=True,blank=True)
    descripcion = models.TextField(blank=True)
    activado = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Tratamiento"
    def __str__(self):
        return self.nombre

class Terapia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=50)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField("Tipo",max_length=50)
    class Meta:
        verbose_name_plural = "Terapia"
    def __str__(self):
        return self.nombre

class Terapia_Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    terapia = models.ManyToManyField(Terapia)
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Terapia_Tratamiento"
    def __str__(self):
        return str(self.terapia)
    def getNombre(id):
        return Terapia.objects.filter(id=id)

class Especialista_Terapia_Tratamiento(models.Model):
    terapia_tratamiento = models.ForeignKey(Terapia_Tratamiento,on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    fecha = models.DateField(null=True,blank=True)
    class Meta:
        verbose_name_plural = "Especialista_Terapia_Tratamiento"
        unique_together = ("terapia_tratamiento","especialista","fecha")

class Supervisa(models.Model):
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Supervisa"
        unique_together = ("especialista","tratamiento")

class Diagnostico(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = datetime.today()
    valoracion = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Diagnostico"

class Sesion(models.Model):
    id = models.AutoField(primary_key=True)
    terapia_tratamiento = models.ForeignKey(Terapia_Tratamiento,on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Sesion"

class Terapia_Actividad(models.Model):
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    terapia = models.ForeignKey(Terapia,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Terapia_Actividad"
        unique_together = ("actividad","terapia")

class Resultado_Sesion(models.Model):
    sesion = models.ForeignKey(Sesion,on_delete=models.CASCADE)
    indicador = models.ForeignKey(Indicador,on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    resultado =  models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Resultado_Sesion"
        unique_together = ("sesion","indicador","actividad")

class Categoria(models.Model):
    id =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    class Meta:
        verbose_name_plural = "Categoria"
    def __str__(self):
        return self.nombre

class Categoria_Actividad(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categoria_Actividad"
        unique_together = ("categoria","actividad")

class Contenido(models.Model):
    id =  models.AutoField(primary_key=True)
    descripcion =  models.CharField(max_length=50, blank=True)
    codigo = models.CharField(max_length=8, blank=True)
    class Meta:
        verbose_name_plural = "Contenido"
    def __str__(self):
        return self.descripcion

class Multimedia(Contenido):
    nombre = models.CharField(max_length=100)
    audio = models.FileField(upload_to=generarDirectorioSubida, null=True, blank=True)
    video = models.FileField(upload_to=generarDirectorioSubida, null=True, blank=True)
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Multimedia"
        ordering = ('datetime',)

    def __str__(self):
        return self.nombre

class Actividad_Contenido(models.Model):
    actividad= models.ForeignKey(Actividad,on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Actividad_Contenido"
        unique_together = ("actividad","contenido")

class Pregunta(models.Model):
    pregunta = models.TextField(blank=False,null=False)
    formato = models.CharField(max_length=20, choices=Formato, default="Imagen")
    class Meta:
        verbose_name_plural = "Pregunta"
    def __str__(self):
        return self.pregunta

class Pregunta_Matching(Pregunta):
    multimediaPregunta = models.ForeignKey("Multimedia",related_name="multimedia+",blank=False,on_delete=models.CASCADE)
    respuesta = models.ForeignKey("Respuesta",related_name="respuesta+",blank=False,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Pregunta_Matching"
    def __str__(self):
        return "{} : {} : {}".format(self.pregunta,self.multimediaPregunta,self.respuesta)

class Pregunta_Quizz(Pregunta):
    multimediaPregunta = models.ForeignKey("Multimedia",related_name="pregunta+",blank=False,on_delete=models.CASCADE)
    respuestas = models.ManyToManyField("Respuesta",related_name="respuestas+",blank=False)
    visualizacion = models.CharField(max_length=20, choices=Visualizacion, default="Unica")
    class Meta:
        verbose_name_plural = "Pregunta_Quizz"

class Actividad_Pregunta(models.Model):
    id =  models.AutoField(primary_key=True)
    actividad= models.ForeignKey(Actividad,on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("actividad","pregunta")
        verbose_name_plural = "Actividad_Pregunta"

class Respuesta(models.Model):
    multimedia = models.ForeignKey("Multimedia",related_name="multimedia",blank=False,on_delete=models.CASCADE)
    resultado =  models.CharField(max_length=20, choices=Resultado, default="")
    class Meta:
        verbose_name_plural = "Respuesta"
    def __str__(self):
        return "{} : {}".format(self.multimedia,self.resultado)
