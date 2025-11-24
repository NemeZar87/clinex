from django.db import models
from django.conf import settings
from cuenta.models import UsuarioPersonalizado

# Create your models here.
class HistoriaClinica(models.Model):
    ESTADOS_CIVILES = [
        ("soltero/a", "Soltero/a"),
        ("casado/a", "Casado/a"),
        ("divorciado/a", "Divorciado/a"),
        ("viudo/a", "Viudo/a"),
        ("separado/a", "Separado/a"),
    ]

    # Datos personales
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #ocultar
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, choices=ESTADOS_CIVILES,  blank=True, null=True)
    obra_social = models.CharField(max_length=200, blank=True, null=True)

    #Datos medicos previos
    enfermedades_cronicas = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    cirugias_previas = models.TextField(blank=True, null=True)
    hospitalizaciones_previas = models.TextField(blank=True, null=True)
    medicacion_habitual = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()}"


class Consulta(models.Model):
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name="consultas", null=True) #ocultar
    profesional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) #ocultar
    fecha = models.DateTimeField(auto_now_add=True) 
    motivo = models.CharField(max_length=200)
    historia_enfermedad_actual = models.TextField()
    examen_fisico = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    estudios_complementarios = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    evolucion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta {self.fecha.strftime('%d/%m/%Y')} - {self.paciente.usuario.get_full_name()}"