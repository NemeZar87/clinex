# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UsuarioPersonalizado, Paciente, Medico

@receiver(post_save, sender=UsuarioPersonalizado)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.tipo_cuenta == 'paciente':
            Paciente.objects.create(usuario=instance)
        elif instance.tipo_cuenta == 'medico':
            Medico.objects.create(usuario=instance)
