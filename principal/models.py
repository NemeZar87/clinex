from django.db import models

# ==============================
# 1. PROVINCIA
# ==============================
class Provincia(models.Model):
    id_indec = models.CharField(
        max_length=25,
        primary_key=True,
        unique=True,
        verbose_name="ID INDEC"
    )
    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        db_table = 'principal_provincia'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ==============================
# 2. DEPARTAMENTO
# ==============================
class Departamento(models.Model):
    id_indec = models.CharField(
        max_length=25,
        primary_key=True,
        unique=True,
        verbose_name="ID INDEC"
    )
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name='departamentos'
    )

    class Meta:
        db_table = 'principal_departamento'
        ordering = ['nombre']
        unique_together = ('nombre', 'provincia')

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"


# ==============================
# 3. LOCALIDAD
# ==============================
class Localidad(models.Model):
    id_indec = models.CharField(
        max_length=25,
        primary_key=True,
        unique=True,
        verbose_name="ID INDEC"
    )
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='localidades'
    )

    class Meta:
        db_table = 'principal_localidad'
        ordering = ['nombre']
        unique_together = ('nombre', 'departamento')

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"