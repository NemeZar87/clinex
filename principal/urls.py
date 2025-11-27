from django.urls import path
from . import views

app_name = 'principal'

urlpatterns = [
    path("", views.index, name="index"),
    path("perfil_medico/<int:medico_id>/", views.perfil_medico, name="perfil_medico"),
    path("ajax/departamentos/<int:prov_id>/", views.ajax_departamentos, name="ajax_departamentos"),
    path("ajax/localidades/<str:dep_id>/", views.ajax_localidades, name="ajax_localidades"),
]