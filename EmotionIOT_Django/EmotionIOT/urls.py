from django.conf.urls import url, include
from django.contrib import admin

from . import views
from EmotionIOT.views import Inicio

# For load images in dev mode
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', Inicio.as_view(), name='Inicio'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
