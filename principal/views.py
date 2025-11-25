from django.shortcuts import render
from cuenta.models import UsuarioPersonalizado
from cuenta.models import Medico, HorarioTrabajo
from principal.models import Departamento, Localidad, Provincia 
from django.http import JsonResponse, HttpResponse
# Create your views here.

def index(request):
    medicos_qs = UsuarioPersonalizado.objects.filter(tipo_cuenta='medico')
    ctx = {
        "medicos": medicos_qs,
    }
    return render(request, "principal/index.html", ctx)


def perfil_medico(request):
    medico_id = 1 #esto tiene que llegar de los filtos, solo sirve para pruebas.
    medico_qs = HorarioTrabajo.objects.filter(medico_id=medico_id) #agregar filtro por depto
    lista_medico = list(medico_qs)
    try:
        medico_all = lista_medico[0].medico
    except IndexError:
        return HttpResponse("asd")
    lugares = []
    for j in medico_qs:
        lugar_all = j.lugar
        dicc_temp = {
            "insti" : lugar_all.nombre,
            "direc" : lugar_all.direccion,
            "tel" : lugar_all.telefono,
        }
        lugares.append(dicc_temp)
    # print(lugares)
    ctx = {
        "medico" : medico_all,
        "lugares" : lugares,
    }
    return render(request, "principal/perfil_medico.html", ctx)

    # {{ for lugar in lugares }}
    #     {{ for j in lugar }}
    #         <p> {{ j.insti }} </p>
    #         <p> {{ j.direc }} </p>
    #         <p> {{ j.tel }} </p>
    #     {{ endfor }}
    # {{ endfor }}

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