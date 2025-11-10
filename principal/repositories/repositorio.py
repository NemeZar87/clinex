from cuenta.models import Medico

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

