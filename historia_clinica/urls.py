from django.urls import path
from . import views

urlpatterns = [
    path("", views.historia_clinica, name="historia-clinica"),
    path("lista_pacientes/", views.lista_paciente, name="lista-pacientes"),
]