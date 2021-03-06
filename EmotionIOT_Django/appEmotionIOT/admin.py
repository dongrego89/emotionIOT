"""!
@package admin.py
@brief Archivo de models registrados para administrar de appEmotionIOT
@author Gregorio Corpas Prieto
@date 13/03/2019
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actividad, Multimedia, Paciente, Especialista, Terapia, Tratamiento
from .models import Terapia_Tratamiento, Especialista_Terapia_Tratamiento, Supervisa, Diagnostico
from .models import Sesion, Indicador, Terapia_Actividad, Resultado_Sesion, Categoria, Categoria_Actividad
from .models import Contenido, Pregunta, Pregunta_Matching, Pregunta_Quiz, Actividad_Pregunta, Respuesta
from .models import Registro_Sesion


# Register your models here
admin.site.register(Actividad)
admin.site.register(Registro_Sesion)
admin.site.register(Respuesta)
admin.site.register(Multimedia)
admin.site.register(Paciente)
admin.site.register(Especialista)
admin.site.register(Terapia)
admin.site.register(Tratamiento)
admin.site.register(Especialista_Terapia_Tratamiento)
admin.site.register(Supervisa)
admin.site.register(Diagnostico)
admin.site.register(Sesion)
admin.site.register(Indicador)
admin.site.register(Terapia_Actividad)
admin.site.register(Resultado_Sesion)
admin.site.register(Categoria)
admin.site.register(Categoria_Actividad)
admin.site.register(Contenido)
admin.site.register(Terapia_Tratamiento)
admin.site.register(Pregunta)
admin.site.register(Pregunta_Matching)
admin.site.register(Pregunta_Quiz)
admin.site.register(Actividad_Pregunta)
