from django.contrib.auth.models import User

def guardar_usuario(form):
    user = form.save()
    return user