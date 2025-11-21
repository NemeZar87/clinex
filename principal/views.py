from django.shortcuts import render
from django.http import HttpResponse
from cuenta.models import UsuarioPersonalizado, HorarioTrabajo
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

def perfil_medico(request):
    medico_id = 1 #esto tiene que llegar de los filtos, solo sirve para pruebas.
    medico_qs = HorarioTrabajo.objects.filter(medico_id=medico_id) #agregar filtro por depto
    lista_medico = list(medico_qs)
    medico_all = lista_medico[0].medico
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

