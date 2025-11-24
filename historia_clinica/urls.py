from django.urls import path
from . import views

app_name = 'historia_clinica'

urlpatterns = [
    path("", views.historia_clinica_view, name="historia_clinica"),
    path("lista_pacientes/", views.lista_paciente, name="lista-pacientes"),
    path("nueva_consulta/<int:paciente_id>/", views.crear_consulta, name="crear_consulta"),
    path("detalle_paciente/<int:paciente_id>/", views.detalle_paciente, name="detalle_paciente"),
    path("cargar_datos/<int:paciente_id>/", views.cargar_datos, name="cargar_datos"),
    path("ver_consulta/<int:consulta_id>/", views.ver_consulta, name="ver_consulta"),
    path("mi_historia/", views.mi_historia_clinica, name="mi_historia"),
]