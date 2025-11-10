from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def medico_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si el usuario autenticado tiene un perfil de médico
        if hasattr(request.user, 'medico'):
            return view_func(request, *args, **kwargs)
        # Si no es médico, redirigimos o mostramos error
        return redirect('no_autorizado')  # o usa HttpResponseForbidden()
    return _wrapped_view
