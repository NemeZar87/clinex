from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearCuenta, InicioSesion
from cuenta.services.servicios import crear_cuenta, iniciar_sesion, cerrar_sesion, medico_required
from .services.lector_dni import lector_total
from principal.models import Provincia, Departamento, Localidad
from django.http import JsonResponse
from cuenta.models import UsuarioPersonalizado
from turno.models import Turno


def crear_cuenta_view(request):
    if request.method == "POST":
        form = CrearCuenta(request.POST, request.FILES)
        if form.is_valid():
            # lector = lector_total(request, form)
            # if lector is None:
            #     ctx = {
            #         "form" : form,
            #         "errors" : "Error de imagen"
            #     }
            #     return render(request, "cuenta/registro.html", ctx)
            # elif lector == True:
            crear_cuenta(request, form)
            return redirect("principal:index")
            # elif lector == False:
            #     ctx = {
            #     "form" : form,
            #     "errors" : "Error: Los datos ingresados no coinciden con lo leido. Vuelva a intentarlo."
            #     }
            #     return render(request, "cuenta/registro.html", ctx)
        else:
            ctx = {"form": form}
            return render(request, "cuenta/registro.html", ctx)
    else:
        form = CrearCuenta()
        ctx = {"form": form}
        return render(request, "cuenta/registro.html", ctx)

def inicio_sesion_view(request):
    if request.method == "POST":
        form = InicioSesion(request, data=request.POST)
        if form.is_valid():
            iniciar_sesion(request, form)
            return redirect("principal:index")
        else:
            ctx = {"form": form}
            return render(request, "cuenta/inicio_sesion.html", ctx)
    else:
        form = InicioSesion()
        ctx = {"form": form}
        return render(request, "cuenta/inicio_sesion.html", ctx)

def cerrar_sesion_view(request):
    cerrar_sesion(request)
    return redirect("principal:index")

def contacto_view(request):
    return render(request, "cuenta/contacto.html")

def servicios_view(request):
    return render(request, "cuenta/servicios.html")

def turnos_view(request):
    paciente = get_object_or_404(UsuarioPersonalizado, username=request.user.username)
    turnos_asignados = Turno.objects.filter(paciente_nombre_id=paciente.id)
    lista_turnos = list(turnos_asignados)
    todo = []
    for turno in lista_turnos:
        medico_all = turno.medico
        fecha_turno= turno.inicio

        temp =  {
            "medico": medico_all,
            "fecha":fecha_turno

        }
        todo.append(temp)
    
    if todo:
        reserva = True
    else:
        reserva = False
    
    ctx = {
        "turnos": todo,
        "reserva": reserva,
    }
    return render(request, "cuenta/turnos.html", ctx)


@medico_required
def configuracion_medica_view(request):
    medico = request.user.medico

    # PRESELECCIONES
    localidad_actual = medico.localidad
    departamento_actual = localidad_actual.departamento if localidad_actual else None
    provincia_actual = departamento_actual.provincia if departamento_actual else None

    provincias = Provincia.objects.all()

    if request.method == "POST":
        loc_id = request.POST.get("localidad")
        if loc_id:
            medico.localidad_id = loc_id
            medico.save()
        return redirect('cuenta:config_medica')

    ctx = {
        "medico": medico,
        "provincias": provincias,
        "provincia_actual": provincia_actual,
        "departamento_actual": departamento_actual,
        "localidad_actual": localidad_actual,
    }

    return render(request, "cuenta/config_medica.html", ctx)



def configuracion_perfil_view(request):
    return render(request, "cuenta/config_perfil.html")

def cronograma(request):
    return render(request, "cuenta/cronograma.html")

def aspecto(request):
    return render(request, "cuenta/aspecto.html")

from django.http import JsonResponse


def filtrar_departamentos(request, prov_id):
    # Devuelve id_indec y nombre, que es lo que espera el JS
    data = list(Departamento.objects.filter(provincia_id=prov_id).values("id_indec", "nombre"))
    return JsonResponse(data, safe=False)

def filtrar_localidades(request, dep_id):
    # Devuelve id_indec y nombre
    data = list(Localidad.objects.filter(departamento_id=dep_id).values("id_indec", "nombre"))
    return JsonResponse(data, safe=False)