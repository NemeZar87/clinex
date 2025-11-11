from django.shortcuts import render
from django.http import HttpResponse
from cuenta.models import UsuarioPersonalizado
from django.shortcuts import render
# from principal.services.servicios import obtener_medicos_filtrados
# Create your views here.


def index(request):
    print("test")
    medicos_qs = UsuarioPersonalizado.objects.filter(tipo_cuenta='medico')
    print(medicos_qs)

    for j in medicos_qs:
        print(f"JOTA: {j}")

    ctx = {
        "medicos": medicos_qs,
    }
    return render(request, "principal/index.html", ctx)

def lista_medicos(request):
    localidad = request.GET.get('localidad')
    institucion = request.GET.get('institucion')
    especialidad = request.GET.get('especialidad')

    # medicos = obtener_medicos_filtrados(localidad, institucion, especialidad)
    # return render(request, 'medicos/lista_medicos.html', {'medicos': medicos})


