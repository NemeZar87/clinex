from cuenta.models import Medico
from principal.models import GobiernoLocal, Localidad

def filtrar_medicos(localidad=None, institucion=None, especialidad=None):
    queryset = Medico.objects.all()

    if especialidad:
        queryset = queryset.filter(especialidad__icontains=especialidad)

    # Filtrar por LugarTrabajo a través del horario
    if localidad or institucion:
        queryset = queryset.filter(horario__lugar__isnull=False).distinct()
        if localidad:
            queryset = queryset.filter(horario__lugar__direccion__icontains=localidad)
        if institucion:
            queryset = queryset.filter(horario__lugar__nombre__icontains=institucion)

    return queryset.distinct()


def guardar_gobierno_local(id, nombre):
    #Crea o recupera un GobiernoLocal existente.
    gobierno_local, _ = GobiernoLocal.objects.get_or_create(
        id=id,
        defaults={"nombre": nombre}
    )
    return gobierno_local


def guardar_localidad(id, nombre, gobierno_local):
    #Crea o recupera una Localidad asociada a un GobiernoLocal.
    localidad, _ = Localidad.objects.get_or_create(
        id=id,
        defaults={
            "nombre": nombre,
            "gobierno_local": gobierno_local
        }
    )
    return localidad


