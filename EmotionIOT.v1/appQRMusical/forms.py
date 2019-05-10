# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia, Actividad, Paciente, Especialista, Tratamiento, Diagnostico, Terapia, Asigna_Terapia, Indicador, Contenido, Categoria, Categoria_Actividad, Terapia_Actividad
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

YEARS= [x for x in range(1990,2021)]

# Create your tests here.

#Formulario para elementos multimedia

class UploadMultimediaForm(forms.ModelForm):
	class Meta:
		model = Multimedia
		fields = ['audio', 'imagen']

	def __init__(self, *args, **kwargs):
		super(UploadMultimediaForm, self).__init__(*args, **kwargs)
		self.fields['audio'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})
		self.fields['imagen'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})

#Formulario para Actividades

class FormularioActividad(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = ['nombre', 'descripcion','proposito','juego']

	def __init__(self, *args, **kwargs):
		super(FormularioActividad, self).__init__(*args, **kwargs)
		self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
		self.fields['descripcion'].widget.attrs.update({'class' : 'form-control'})
		self.fields['proposito'].widget.attrs.update({'class' : 'form-control'})

#Formulario para Indicadores

class UploadIndicatorForm(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = ['indicador']

	def __init__(self, *args, **kwargs):
		super(UploadIndicatorForm, self).__init__(*args, **kwargs)
		self.fields['indicador'].widget.attrs.update({'class' : 'selectpicker'})

#Formulario para Pacientes

class UploadUserForm(forms.ModelForm):
	class Meta:
		model = Paciente
		fields = ['imagen','nombre', 'apellido','fecha_de_nacimiento','genero','nivel']

	def __init__(self, *args, **kwargs):
		super(UploadUserForm, self).__init__(*args, **kwargs)
		self.fields['imagen'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})
		self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
		self.fields['apellido'].widget.attrs.update({'class' : 'form-control'})
		self.fields['fecha_de_nacimiento'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['nivel'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['genero'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})


#Formulario para Especialistas

class FormularioEspecialista(UserCreationForm):
    model = User
    fields = ('username', 'password1', 'password2', )

#Formulario para Tratamientos

class UploadTreatmentForm(forms.ModelForm):
	class Meta:
		model = Tratamiento
		fields = ['paciente','nombre', 'fecha_inicio','fecha_fin','descripcion','activado']

	def __init__(self, *args, **kwargs):
		super(UploadTreatmentForm, self).__init__(*args, **kwargs)
		self.fields['paciente'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
		self.fields['fecha_inicio'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['fecha_fin'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['descripcion'].widget.attrs.update({'class' : 'form-control'})
		self.fields['activado'].widget.attrs.update({'class' : 'custom-control-input'})

#Formulario para Terapias

class UploadTherapyForm(forms.ModelForm):
	class Meta:
		model = Terapia
		fields = ['nombre','descripcion','tipo']

	def __init__(self, *args, **kwargs):
		super(UploadTherapyForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['descripcion'].widget.attrs.update({'class' : 'form-control'})
		self.fields['tipo'].widget.attrs.update({'class' : 'custom-control-input'})

#Formulario para Asignar las Terapias usado en la pantalla de creacion de tratamientos

class UploadAsignTherapyForm(forms.ModelForm):
    terapia = forms.ModelMultipleChoiceField(queryset=Terapia.objects.all(),required=False)
    class Meta:
        model = Asigna_Terapia
        fields = ['terapia']

    def __init__(self, *args, **kwargs):
        super(UploadAsignTherapyForm, self).__init__(*args, **kwargs)
        self.fields['terapia'].widget.attrs.update({'class' : 'selectpicker'})


#Formulario para Asignar los Tratamientos usado en la pantalla de creacion de Terapias

class UploadAsign(forms.ModelForm):
    tratamiento = forms.ModelChoiceField(queryset=Tratamiento.objects.all(),required=False)
    class Meta:
        model = Asigna_Terapia
        fields = ['tratamiento']

    def __init__(self, *args, **kwargs):
        super(UploadAsign, self).__init__(*args, **kwargs)
        self.fields['tratamiento'].widget.attrs.update({'class' : 'selectpicker'})

#Formulario para los Diagnosticos

class UploadDiagnosticForm(forms.ModelForm):
	class Meta:
		model = Diagnostico
		fields = ['valoracion','notas']

	def __init__(self, *args, **kwargs):
		super(UploadDiagnosticForm, self).__init__(*args, **kwargs)
		self.fields['valoracion'].widget.attrs.update({'class' : 'form-control'})
		self.fields['notas'].widget.attrs.update({'class' : 'form-control'})

#Formulario para las categorias

class UploadCategoryForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['nombre']

	def __init__(self, *args, **kwargs):
		super(UploadCategoryForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})

#Formulario para Asignar las categorias con las actividades

class FormularioCategoriaActividad(forms.ModelForm):
	class Meta:
		model = Categoria_Actividad
		fields = ['actividad','categoria']

	def __init__(self, *args, **kwargs):
		super(FormularioCategoriaActividad, self).__init__(*args, **kwargs)
		self.fields['actividad'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['categoria'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})

#Formulario para Vincular las Actividades con las Terapias

class UploadTherapyFormActividad(forms.ModelForm):
	class Meta:
		model = Terapia_Actividad
		fields = ['actividad','terapia']

	def __init__(self, *args, **kwargs):
		super(UploadTherapyFormActividad, self).__init__(*args, **kwargs)
		self.fields['actividad'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['terapia'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})

#Formulario para Vincular una Terapias con una actividad durante la creación de la actividad

class UploadOnePlayerTerapiaForm(forms.ModelForm):
	terapia = forms.ModelChoiceField(queryset=Terapia.objects.all(),required=False)
	class Meta:
		model = Terapia_Actividad
		fields = ['terapia']

	def __init__(self, *args, **kwargs):
		super(UploadOnePlayerTerapiaForm, self).__init__(*args, **kwargs)
		self.fields['terapia'].widget.attrs.update({'class' : 'form-control'})

#Formulario para Vincular una Terapias con una actividad durante la creación de la terapia

class UploadOneActividadTherapyForm(forms.ModelForm):
	actividad = forms.ModelChoiceField(queryset=Actividad.objects.all(),required=False)
	class Meta:
		model = Terapia_Actividad
		fields = ['actividad']

	def __init__(self, *args, **kwargs):
		super(UploadOneActividadTherapyForm, self).__init__(*args, **kwargs)
		self.fields['actividad'].widget.attrs.update({'class' : 'selectpicker'})

#Formulario para editar Nombre y Apellidos del especialista

class EditNameForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Get request"""
        self.request = kwargs.pop('request')
        return super(EditNameForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name
    def clean_surname(self):
        surname = self.cleaned_data['surname']
        return surname

#Formulario para el email del especialista

class EditEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Get request"""
        self.request = kwargs.pop('request')
        return super(EditEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Change email?
        last_email = self.request.user.email
        username = self.request.user.username
        if email != last_email:
            # If doesnt exists in BD
            exists = User.objects.filter(email=email).exclude(username=username)
            if exists:
                raise forms.ValidationError('This emails is already registed.')
        return email

#Formulario para editar la contraseña especialista

class EditPassForm(forms.Form):
    last_password = forms.CharField(
        label='Contraseña actual',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repita contraseña',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Match pass1 & pass2."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('The passwords doesn\'t be equal.')
        return password2
