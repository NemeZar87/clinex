from django.db import models
from cuenta.models import UsuarioPersonalizado, Medico

# Create your models here.


class Turno(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="turnos")
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    paciente_nombre = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True, related_name="turnos")
    creado = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["inicio"]
    
    def __str__(self):
        estado = "Ocupado" if self.esta_ocupado() else "Libre"
        return f"{self.medico} - {self.inicio} ({estado})" 
    
    def esta_ocupado(self):
        return self.paciente_nombre is not None
