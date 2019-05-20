from django.conf.urls import url, include
from django.contrib import admin

from appQRMusical.views import Desconectar, Settings, Game_settings, ElegirActividad, Gallery, Multimedia_detail, Multimedia_delete, Actividads_list, Users_list, Update_player, Update_user, User_ID, Multi_ID, Multi_ID_delete, Create_player, Create_user, Multimedia_update, Actividad_delete, ID_delete, User_delete, User, Especialistas_list, Tratamientos_list, Therapies_list, Create_therapist, Create_treatment, Tratamiento_delete, Update_treatment, Diagnostico_list, Create_diagnostic, Update_diagnostic, Delete_diagnostic, Create_therapy, Update_therapy, Terapia_delete, Activity_settings,Lista_Indicadores, Create_indicator, Update_indicator, Indicador_delete, Categories_list, Update_category, Categoria_delete, Create_category, Add_category_player, Resultados, Resultados_details, Add_therapy_player, Terapia_player_list,  Delete_therapy_player, Summary, ResultadosTratamiento, ElegirTerapia, LoginPacientes

from . import views


# For load images in dev mode
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', LoginPacientes.as_view(), name='loginpacientes'),
	url(r'^prueba$', views.prueba, name='prueba'),

	url(r'^desconectar/$', Desconectar, name='desconectar'),
	url(r'^rfidlogin/$', views.RFIDLogin, name='rfidlogin'),

	# Play-Songs
	url(r'^elegirTerapia/$', ElegirTerapia.as_view(), name='elegirTerapia'),
	url(r'^elegirActividad/(?P<idTerapia>\d+)/(?P<idTerapiaTratamiento>\d+)/$', ElegirActividad, name='elegirActividad'),

    # Login
	url(r'^login/$', views.Login, name='login'),
	url(r'^logout/$', views.Logout, name='logout'),

	#Quizz
	url(r'^quizz/(?P<idActividad>\d+)/(?P<idAsignaTerapia>\d+)/$', views.Quizz, name='quizz'),
	url(r'^quizz/$', views.QuizzCallBack, name='quizzCallBack'),

	url(r'^matching/(?P<idActividad>\d+)/(?P<idTerapiaTratamiento>\d+)/(?P<idTerapia>\d+)/$', views.Matching, name='matching'),
	url(r'^matching/$', views.MatchingCallBack, name='matchingCallBack'),


	# Settings
	url(r'^settings/$', Settings.as_view(), name='settings'),
	url(r'^settings/Activities/$', Activity_settings.as_view(), name='activity_settings'),
	url(r'^settings/Games/$', Game_settings.as_view(), name='game_settings'),
	url(r'^settings/Categories/$', Categories_list.as_view(), name='categories_list'),
	url(r'^settings/Categories/(?P<pk>\d+)/update/$', Update_category.as_view(), name='update_category'),
	url(r'^settings/Categories/(?P<pk>\d+)/delete/$', Categoria_delete.as_view(), name='category_delete'),
	url(r'^settings/Categories/create/$', Create_category.as_view(), name='create_category'),

	# Settings - Therapy-Activity
	url(r'^settings/Activities/therapy-player/$', Terapia_player_list.as_view(), name='therapy_player'),
	url(r'^settings/Activities/therapy-player/details/$', Add_therapy_player.as_view(), name='add_therapy_player'),
	url(r'^settings/Activities/therapy-player/(?P<pk>\d+)/delete/$', Delete_therapy_player.as_view(), name='delete_therapy_player'),

	# Settings - Results
	url(r'^settings/Results/$', Resultados.as_view(), name='results'),
	url(r'^settings/Results/Treatment/(?P<pk>\d+)/$', ResultadosTratamiento, name='results_treatment'),
	url(r'^settings/Results/(?P<pk>\d+)/Details/$', Resultados_details, name='results_details'),

	# Settings - Gallery
	url(r'^settings/gallery/$', Gallery.as_view(), name='gallery'),
	url(r'^settings/gallery/multimedia_detail/(?P<pk>\d+)/$', Multimedia_detail.as_view(), name='multimedia_detail'),
	url(r'^settings/gallery/multimedia_update/(?P<pk>\d+)/$', Multimedia_update.as_view(), name='multimedia_update'),
	url(r'^settings/gallery/(?P<pk>\d+)/delete/$', Multimedia_delete.as_view(), name='multimedia_delete'),
	url(r'^settings/gallery/upload/$', views.upload_multimedia, name='upload_multimedia'),
	url(r'^settings/gallery/multimedia_id/(?P<pk>\d+)/$', Multi_ID, name='multi_id'),
	url(r'^settings/gallery/multimedia_id_clean/(?P<pk>\d+)/$', Multi_ID_delete, name='multi_id_delete'),

	# Settings - Music Game
	url(r'^settings/players_list/$', Actividads_list.as_view(), name='players_list'),
	url(r'^settings/players_list/(?P<pk>\d+)/update/$', Update_player.as_view(), name='update_player'),
	url(r'^settings/players_list/category_player/$', Add_category_player.as_view(), name='add_category_player'),
	url(r'^settings/players_list/(?P<pk>\d+)/delete/$', Actividad_delete.as_view(), name='player_delete'),
	url(r'^settings/players_list/create/$', Create_player, name='create_player'),
	url(r'^settings/players_list/(?P<id>\d+)/add_multimedia_to_player/$', views.add_multimedia_to_player, name='add_multimedia_to_player'),
	url(r'^settings/players_list/(?P<id_player>\d+)/add_multimedia_to_player/(?P<id_multimedia>\d+)/$', views.add_multimedia_to_player_function, name='add_multimedia_to_player_function'),
	url(r'^settings/players_list/(?P<id_player>\d+)/update/(?P<id_multimedia>\d+)/$', views.del_multimedia_of_player_function, name='del_multimedia_of_player_function'),

	# Settigns - User
	url(r'^settings/user/$', User.as_view(), name='user'),
	url(r'^settings/user/edit_name/$', views.edit_name, name='edit_name'),
	url(r'^settings/user/edit_email/$', views.edit_email, name='edit_email'),
	url(r'^settings/user/edit_password/$', views.edit_password, name='edit_password'),

    # Settigns - Users
	url(r'^settings/users_list/$', Users_list.as_view(), name='users_list'),
	url(r'^settings/users_list/(?P<pk>\d+)/update/$', Update_user.as_view(), name='update_user'),
	url(r'^settings/users_list/(?P<pk>\d+)/modID/$', User_ID, name='user_id'),
	url(r'^settings/users_list/(?P<pk>\d+)/delete/$', User_delete.as_view(), name='user_delete'),
	url(r'^settings/users_list/(?P<pk>\d+)/IDdelete/$', ID_delete, name='id_delete'),
	url(r'^settings/users_list/create/$', Create_user.as_view(), name='create_user'),

    # Settigns - Treatments
	url(r'^settings/treatments_list/$', Tratamientos_list, name='treatments_list'),
	url(r'^settings/treatments_list/create/$', Create_treatment, name='create_treatment'),
	url(r'^settings/treatmentss_list/(?P<pk>\d+)/update/$', Update_treatment.as_view(), name='update_treatment'),
	url(r'^settings/treatmentss_list/(?P<pk>\d+)/delete/$', Tratamiento_delete.as_view(), name='treatment_delete'),

    # Settigns - Therapies
	url(r'^settings/therapies_list/$', Therapies_list, name='therapies_list'),
	url(r'^settings/therapies_list/create$', Create_therapy, name='create_therapy'),
	url(r'^settings/therapies_list/(?P<pk>\d+)/update$', Update_therapy.as_view(), name='update_therapy'),
	url(r'^settings/therapies_list/(?P<pk>\d+)/delete$', Terapia_delete.as_view(), name='therapy_delete'),

    # Settigns - Diagnostic
	url(r'^settings/user/(?P<pk>\d+)/diagnostic_list/$', Diagnostico_list, name='diagnostic_list'),
	url(r'^settings/user/(?P<pk>\d+)/diagnostic_create/$', Create_diagnostic, name='create_diagnostic'),
	url(r'^settings/user/(?P<pk>\d+)/update_diagnostic/$', Update_diagnostic.as_view(), name='update_diagnostic'),
	url(r'^settings/user/(?P<pk>\d+)/delete_diagnostic/$', Delete_diagnostic.as_view(), name='delete_diagnostic'),

	#Settigns - Therapists
	url(r'^settings/therapists_list/$', Especialistas_list, name='therapists_list'),
	url(r'^settings/create_therapists/$', Create_therapist.as_view(), name='create_therapist'),

	#Settings - Indicators
	url(r'^settings/activities/indicators/$', Lista_Indicadores.as_view(), name='indicators_list'),
	url(r'^settings/activities/indicators/create/$', Create_indicator.as_view(), name='create_indicator'),
	url(r'^settings/activities/indicators/(?P<pk>\d+)/update/$', Update_indicator.as_view(), name='update_indicator'),
	url(r'^settings/activities/indicators/(?P<pk>\d+)/delete/$', Indicador_delete.as_view(), name='indicator_delete'),

	#Settings - Summary
	url(r'^settings/activities/summary/$', Summary, name='summary'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
