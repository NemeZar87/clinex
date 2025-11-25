from django.shortcuts import render
from cuenta.models import UsuarioPersonalizado
from cuenta.models import Medico
from principal.models import Departamento, Localidad, Provincia 
from django.http import JsonResponse
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



def index(request):
    provincias = Provincia.objects.all()

    medicos = Medico.objects.select_related(
        "localidad",
        "localidad__departamento",
        "localidad__departamento__provincia",
        "usuario"
    )

    prov_id = request.GET.get("provincia")
    dep_id = request.GET.get("departamento")
    loc_id = request.GET.get("localidad")

    if loc_id:
        medicos = medicos.filter(localidad_id=loc_id)
    elif dep_id:
        medicos = medicos.filter(localidad__departamento_id=dep_id)
    elif prov_id:
        medicos = medicos.filter(localidad__departamento__provincia_id=prov_id)

    ctx = {
        "provincias": provincias,
        "medicos": medicos
    }

    return render(request, "principal/index.html", ctx)


def ajax_departamentos(request, prov_id):
    departamentos = Departamento.objects.filter(provincia_id=prov_id).values("id", "nombre")
    return JsonResponse(list(departamentos), safe=False)

def ajax_localidades(request, dep_id):
    localidades = Localidad.objects.filter(departamento_id=dep_id).values("id_indec", "nombre")
    
    res = [{"id": loc["id_indec"], "nombre": loc["nombre"]} for loc in localidades]
    return JsonResponse(res, safe=False)