from django.urls import path
from . import views

app_name = 'turno'

urlpatterns = [
    path("", views.turno, name="turno"),
    path("calendario/<int:medico_id>", views.calendario, name="calendario"),
    path("crear/<int:year>/<int:month>/<int:day>/", views.crear_turno, name="crear_turno"),
    
]
