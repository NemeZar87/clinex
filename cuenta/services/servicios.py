from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render
from cuenta.repositories import repositorio

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