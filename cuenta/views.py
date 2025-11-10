from django.shortcuts import render, redirect
from .forms import CrearCuenta, InicioSesion
from cuenta.services.servicios import crear_cuenta, iniciar_sesion, cerrar_sesion, medico_required
from .services.lector_dni import lector_total
# from principal.services.servicios import guardar_localidades, obtener_todas_localidades, obtener_todos_gobiernos_locales

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
    return render(request, "cuenta/turnos.html")

def historia_clinica_view(request):
    return render(request, "cuenta/historia_clinica.html")

@medico_required
def configuracion_medica_view(request):
    # Guardar datos de la API (puede hacerse una vez o con cron)
    guardar_localidades()

    medico = request.user.medico
    horarios = medico.horario.select_related("lugar")
    localidades = obtener_todas_localidades()
    gobiernos = obtener_todos_gobiernos_locales()

    if request.method == "POST":
        localidad_id = request.POST.get("localidad")
        gobierno_local_id = request.POST.get("gobierno_local")

        if localidad_id or gobierno_local_id:
            medico.localidad_id = localidad_id if localidad_id else medico.localidad_id
            medico.gobierno_local_id = gobierno_local_id if gobierno_local_id else medico.gobierno_local_id
            medico.save()
            return redirect('cuenta:config_medica')

    ctx = {
        "medico": medico,
        "horarios": horarios,
        "localidades": localidades,
        "gobiernos": gobiernos,
    }
    return render(request, "cuenta/config_medica.html", ctx)


def configuracion_perfil_view(request):
    return render(request, "cuenta/config_perfil.html")

def cronograma(request):
    return render(request, "cuenta/cronograma.html")

def aspecto(request):
    return render(request, "cuenta/aspecto.html")
