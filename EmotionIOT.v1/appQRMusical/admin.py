# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actividad, Multimedia, Paciente, Especialista, Terapia, Tratamiento
from .models import Terapia_Tratamiento, Especialista_Terapia_Tratamiento, Supervisa, Diagnostico
from .models import Sesion, Indicador, Terapia_Actividad, Resultado_Sesion, Categoria, Categoria_Actividad
from .models import Contenido, Actividad_Contenido
from .models import Pregunta, Pregunta_Matching, Pregunta_Quizz, Actividad_Pregunta, Respuesta

#, Terapia_Indicador  Texto,


# Register your models here. Qui,Quises,
admin.site.register(Actividad)
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
admin.site.register(Actividad_Contenido)
admin.site.register(Terapia_Tratamiento)
admin.site.register(Pregunta)
admin.site.register(Pregunta_Matching)
admin.site.register(Pregunta_Quizz)
admin.site.register(Actividad_Pregunta)
