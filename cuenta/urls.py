from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'cuenta'

urlpatterns = [
    path("inicio_sesion/", views.inicio_sesion_view, name="inicio-sesion"),
    path("registro/", views.crear_cuenta_view, name="registro"),
    path("contacto/", views.contacto_view, name="contacto"),
    path("servicios/", views.servicios_view, name="servicios"),
    path("turnos/", views.turnos_view, name="turnos"),
    path("historia_clinica/", views.historia_clinica_view, name="historia_clinica"),
    path("config_medica/", views.configuracion_medica_view, name="config_medica"),
    path("perfil/", views.configuracion_perfil_view, name="config_perfil"),
    path("cerrar_sesion/", views.cerrar_sesion_view, name="cerrar_sesion"),
    path("cronograma/", views.cronograma, name="cronograma"),
    path("aspecto/", views.aspecto, name="aspecto"),
    path("nueva_consulta/<int:paciente_id>/", views.crear_consulta, name="crear_consulta"),
    path("detalle_paciente/<int:paciente_id>/", views.detalle_paciente, name="detalle_paciente"),
]