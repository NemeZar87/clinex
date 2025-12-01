from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearCuenta, InicioSesion, HorarioTrabajoForm
from cuenta.services.servicios import crear_cuenta, iniciar_sesion, cerrar_sesion, medico_required
# from .services.lector_dni import lector_total
from principal.models import Provincia, Departamento, Localidad
from django.http import JsonResponse
from cuenta.models import UsuarioPersonalizado
from turno.models import Turno
from principal.models import Provincia, Departamento, Localidad
import inspect

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

########################################################

    # HTML: valor.0 == *medico? | valor.1 == *texto visible | valor.2 == *ruta | valor.2 == activo o no
    # Python:
    #   "nombre de la view de la pagina": // ejemplo: def "turnos_views"() - 
    #       "medico?", // buleano para saber si la opcion es de medico 
    #       "Texto visible", // Ejemplo: "Configuracion medica",
    #       "ruta de la pagina", // Ejemplo: "cuenta:config_medica",
    #       "seleccionado?" // valor buleano para saber si es un ancla o no // True o False // NO MODIFICAR, DEJENLO EN True SIEMPRE!
    #   }

########################################################
op_perfil = {
    "turnos_view": [
        False,
        "Turnos",
        "cuenta:turnos",
        True
    ],
    "historia_clinica": [
        False,
        "Historia clinica",
        "historia_clinica:historia_clinica",
        True
        ],
    "configuracion_medica_view": [
        True,
        "Configuración medica",
        "cuenta:config_medica",
        True
        ],
    "configuracion_perfil_view": [
        False,
        "Configuración de perfil",
        "cuenta:config_perfil",
        True
        ],
    "mi_historia_clinica": [
        False,
        "Mi historia clinica",
        "historia_clinica:mi_historia",
        True
        ],
    # "aspecto": [
    #     False,
    #     "Aspecto",
    #     "cuenta:aspecto",
    #     True
    # ],
    # "acerca_de": [
    #     False,
    #     "Acerca de nosotros",
    #     "",
    #     True
    # ]
}
def opciones_perfil():
    for l in op_perfil:
        op_perfil[l][3] = True
    f_name = inspect.stack()[1]
    if f_name.function in op_perfil:
        op_perfil[f_name.function][3] = False
    return op_perfil
################################################################################

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
        "opciones": opciones_perfil(),
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
        # Guardar horario
        if "nuevo_horario" in request.POST:
            form = HorarioTrabajoForm(request.POST, medico=medico)
            if form.is_valid():
                horario = form.save(commit=False)
                horario.medico = medico
                horario.save()
                return redirect('cuenta:config_medica')

        # Guardar localidad
        if "localidad" in request.POST:
            loc_id = request.POST.get("localidad")
            if loc_id:
                medico.localidad_id = loc_id
                medico.save()
            return redirect('cuenta:config_medica')

    else:
        form = HorarioTrabajoForm(medico=medico)

    horarios = medico.horario.all()

    ctx = {
        "medico": medico,
        "provincias": provincias,
        "provincia_actual": provincia_actual,
        "departamento_actual": departamento_actual,
        "localidad_actual": localidad_actual,
        "opciones": opciones_perfil(),
        "horarios": horarios,
        "horario_form": form
    }

    return render(request, "cuenta/config_medica.html", ctx)



def configuracion_perfil_view(request):
    return render(request, "cuenta/config_perfil.html", {"opciones": opciones_perfil()})

def cronograma(request):
    return render(request, "cuenta/cronograma.html")

def aspecto(request):
    return render(request, "cuenta/aspecto.html", {"opciones": opciones_perfil()})



def filtrar_departamentos(request, prov_id):
    # Devuelve id_indec y nombre, que es lo que espera el JS
    data = list(Departamento.objects.filter(provincia_id=prov_id).values("id_indec", "nombre"))
    return JsonResponse(data, safe=False)

def filtrar_localidades(request, dep_id):
    # Devuelve id_indec y nombre
    data = list(Localidad.objects.filter(departamento_id=dep_id).values("id_indec", "nombre"))
    return JsonResponse(data, safe=False)