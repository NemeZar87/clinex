from django.contrib.auth.models import User
from cuenta.models import Medico
from principal.models import Localidad, GobiernoLocal

def guardar_usuario(form):
    user = form.save()
    return user

def obtener_medico_por_usuario(usuario):
    #Devuelve el médico asociado a un usuario.
    return Medico.objects.filter(usuario=usuario).first()

def actualizar_localizacion_medico(medico, localidad_id, gobierno_local_id):
    #Actualiza la localidad y el gobierno local del médico.
    localidad = Localidad.objects.filter(id=localidad_id).first()
    gobierno_local = GobiernoLocal.objects.filter(id=gobierno_local_id).first()

    medico.localidad = localidad
    medico.gobierno_local = gobierno_local
    medico.save()
    return medico