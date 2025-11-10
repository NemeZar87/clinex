from django.shortcuts import render
from django.http import HttpResponse
from cuenta.models import UsuarioPersonalizado
from django.shortcuts import render
from principal.services.servicios import obtener_medicos_filtrados
# Create your views here.


def index(request):
    medicos = UsuarioPersonalizado.objects.filter(tipo_cuenta='medico')
    ctx = {
        "medicos": medicos,
    }
    return render(request, "principal/index.html", ctx)

def lista_medicos(request):
    localidad = request.GET.get('localidad')
    institucion = request.GET.get('institucion')
    especialidad = request.GET.get('especialidad')

    medicos = obtener_medicos_filtrados(localidad, institucion, especialidad)
    return render(request, 'medicos/lista_medicos.html', {'medicos': medicos})

