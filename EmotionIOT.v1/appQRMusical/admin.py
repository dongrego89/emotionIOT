# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actividad, Multimedia, Paciente, Especialista, Terapia, Tratamiento, Asigna_Terapia, Especialista_Asigna_Terapia, Supervisa, Diagnostico, Sesion, Indicador, Terapia_Actividad, Resultado_Sesion, Categoria, Categoria_Actividad, Contenido, Actividad_Contenido,Asigna_Terapia

from .models import Pregunta, Pregunta_Matching, Pregunta_Quizz, Actividad_Pregunta

#, Terapia_Indicador  Texto,


# Register your models here. Qui,Quises,
admin.site.register(Actividad)
admin.site.register(Multimedia)
admin.site.register(Paciente)
admin.site.register(Especialista)
admin.site.register(Terapia)
admin.site.register(Tratamiento)
admin.site.register(Especialista_Asigna_Terapia)
admin.site.register(Supervisa)
admin.site.register(Diagnostico)
admin.site.register(Sesion)
admin.site.register(Indicador)
#admin.site.register(Terapia_Indicador)
admin.site.register(Terapia_Actividad)
admin.site.register(Resultado_Sesion)
admin.site.register(Categoria)
admin.site.register(Categoria_Actividad)
admin.site.register(Contenido)
#admin.site.register(Qui)
#admin.site.register(Quises)
#admin.site.register(Texto)
admin.site.register(Actividad_Contenido)
admin.site.register(Asigna_Terapia)
admin.site.register(Pregunta)
admin.site.register(Pregunta_Matching)
admin.site.register(Pregunta_Quizz)
admin.site.register(Actividad_Pregunta)
