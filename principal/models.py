from django.db import models

class GobiernoLocal(models.Model):
    id = models.IntegerField(primary_key=True)  # usamos el ID de la API
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Localidad(models.Model):
    id = models.IntegerField(primary_key=True)  # usamos el ID de la API
    nombre = models.CharField(max_length=200)
    gobierno_local = models.ForeignKey(GobiernoLocal, on_delete=models.CASCADE, related_name="localidades")

    def __str__(self):
        return self.nombre
