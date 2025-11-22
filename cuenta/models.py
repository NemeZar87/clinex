from django.db import models
# importamos desde django, User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import os
from django.conf import settings #importamos settings desde django.confs
from principal.models import Provincia, Departamento, Localidad

# Create your models here.

#Esta funcion define una ruta personalizada para guardar los archivos separados por usuarios.
def ruta_dni(instancia,nombre_de_archivo):
    nombre_usuario = instancia.username
    return os.path.join("foto_dni", nombre_usuario, nombre_de_archivo)

class UsuarioPersonalizado(AbstractUser):
    telefono = models.CharField(max_length=11, null=True)
    TIPOS_CUENTA = [
        ('paciente', 'Paciente'),
        ('medico', 'Medico'),
    ]
    tipo_cuenta = models.CharField(max_length=14, choices=TIPOS_CUENTA, default="paciente")
    numero_dni = models.CharField(max_length=8, null=True)
    foto_dni = models.ImageField(upload_to=ruta_dni, null=True, blank=True) #esta imagen se guarda en la ruta personalizada
    fecha_nacimiento = models.DateField(null=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_cuenta_display()})"

class Medico(models.Model):
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE)
    ESPECIALIDADES = [
        ('medico-clinico', 'Medico clinico'),
        ('traumatologo', 'Traumatologo'),
        ('dentista', 'Dentista'),
    ]
    especialidad = models.CharField(max_length=20, choices=ESPECIALIDADES, default="medico-clinico")
    # localidad = models.ForeignKey(
    #     Localidad,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='medicos'
    # )

    # def __str__(self):
    #     return f"{self.nombre} - {self.localidad.nombre if self.localidad else 'Sin localidad'}"

    #on_delete=models.SET_NULL si se borra la localidad, no borra al médico, solo deja el campo vacío.
    #null=True, blank=True permite editar el perfil sin forzar estos campos.


class Paciente(models.Model):
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE)
    historial_clinico = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"


class LugarTrabajo(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='lugares', null=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class HorarioTrabajo(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo'),
    ]
    dia = models.CharField(max_length=200, null=True, choices=DIAS_SEMANA, default='')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tiempo_turno = models.DurationField(help_text='Duración entre turnos. Ejemplo: 00:20:00 para 20 minutos')

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horario')
    lugar = models.ForeignKey(LugarTrabajo, on_delete=models.CASCADE, related_name='horario')

    class Meta:
        unique_together = ('medico', 'lugar', 'dia', 'hora_inicio', 'hora_fin')
        ordering = ['lugar', 'dia', 'hora_inicio']

    def __str__(self):
        return (
            f"{self.medico} - {self.lugar} ({self.dia}: {self.hora_inicio} a {self.hora_fin}, "
            f"intervalo {self.tiempo_turno})"
        )
    
    def dias_trabajo_list(self):
        """Devuelve lista de ints con los días de trabajo (0..6)."""
        if not self.dia:
            return []
        return [int(j) for j in self.dia.split(",") if j.strip() != ""]

    def horario_valido(self):
        """Comprueba que hora_inicio < hora_fin"""
        return self.hora_inicio < self.hora_fin

#Es un modelo aparte para asociar un usuario con un dni.
class Dni(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas") #ocultar
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