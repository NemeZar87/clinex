from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render
from cuenta.repositories import repositorio, obtener_medico_por_usuario, actualizar_localizacion_medico
from principal.services import obtener_todas_localidades, obtener_todos_gobiernos_locales

def crear_cuenta(request, form):
    user = repositorio.guardar_usuario(form)
    return user


def iniciar_sesion(request, form):
    user = form.get_user()
    login(request, user)
    return user


def cerrar_sesion(request):
    logout(request)


def medico_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, "medico"):
            return view_func(request, *args, **kwargs)
        errors = {
            "error": "Debe tener una cuenta de medico para ingresar a esa sección."
        }
        return render(request, "principal/index.html", errors)
    return _wrapped_view


def actualizar_perfil_medico(usuario, localidad_id, gobierno_local_id):

    #Actualiza la información de localidad y gobierno local del médico asociado al usuario.
    medico = obtener_medico_por_usuario(usuario)
    if not medico:
        raise ValueError("No se encontró un médico asociado a este usuario.")
    
    medico = actualizar_localizacion_medico(medico, localidad_id, gobierno_local_id)
    return medico


def obtener_datos_configuracion_medica(usuario):
    #Devuelve toda la información necesaria para la vista de configuración médica.
    medico = usuario.medico
    localidades = obtener_todas_localidades()
    gobiernos = obtener_todos_gobiernos_locales()
    horarios = medico.horario.select_related("lugar")
    return medico, horarios, localidades, gobiernos