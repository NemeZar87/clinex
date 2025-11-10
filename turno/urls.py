from django.urls import path
from . import views

urlpatterns = [
    path("", views.turno, name="turno"),
    path("calendario/", views.calendario, name="calendario"),
    path("crear/<int:year>/<int:month>/<int:day>/", views.crear_turno, name="crear_turno"),
    
]
