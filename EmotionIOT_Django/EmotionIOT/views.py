# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime, time, date


# Create your views here.

def Inicio:
    context = {}
    context['titulo'] = "Inicio"
    return render(request,'inicio.html',context)
