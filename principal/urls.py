from django.urls import path
from . import views

app_name = 'principal'

urlpatterns = [
    path("", views.index, name="index"),
    path("ajax/departamentos/<str:prov_id>/", views.ajax_departamentos, name="ajax_departamentos"),
    path("ajax/localidades/<str:dep_id>/", views.ajax_localidades, name="ajax_localidades"),
]