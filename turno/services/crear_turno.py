from datetime import datetime, timedelta, time
from django.utils import timezone
from cuenta.models import HorarioTrabajo, Paciente
from .models import Turno
from django.db import IntegrityError, transaction

def generar_turnos_para_medico(medico: HorarioTrabajo, fecha_inicio: datetime.date, fecha_fin: datetime.date):
    
    # Genera turnos para un médico entre fecha_inicio y fecha_fin (incluyentes).
    # - Crea Turno por cada intervalo de duración dentro del horario del día,
    # sólo en los días que el médico trabaja.
    # - No genera turnos fuera de la franja [hora_inicio, hora_fin).
    # - Si sobrescribir_existentes=True, borrará turnos libres en ese rango antes de crear.

    if not medico.horario_valido():
        raise ValueError("Horario inválido: hora_inicio debe ser menor que hora_fin")

    dias_trabajo = medico.dias_trabajo_list()
    dur_min = medico.tiempo_turno

    # Recolectar datetimes (timezone-aware) para usar en la DB
    tz = timezone.get_default_timezone()

    fecha = fecha_inicio
    created = 0
    while fecha <= fecha_fin:
        weekday = fecha.weekday()  # 0 lunes ... 6 domingo
        if weekday in dias_trabajo:
            # Construimos datetime aware a partir del date y horas
            inicio_jornada = datetime.combine(fecha, medico.hora_inicio)
            fin_jornada = datetime.combine(fecha, medico.hora_fin)

            # Hacerlos timezone-aware (Horario correspondiente a la zona horaria)
            inicio_jornada = timezone.make_aware(inicio_jornada, tz)
            fin_jornada = timezone.make_aware(fin_jornada, tz)

            slot_start = inicio_jornada
            while True:
                slot_end = slot_start + timedelta(minutes=dur_min)
                # Aseguramos que el slot no exceda el fin de jornada (slot_end <= fin_jornada)
                if slot_end > fin_jornada:
                    break

                # Crear turno si no existe uno con el mismo inicio para ese médico
                try:
                    with transaction.atomic():
                        # transaction.atomic hace que se ejecute todo el bloque de codigo o no se ejecute nada, es decir, si sale todo bien, commitea; si algo falla, hace rollback.
                        turno, created_flag = Turno.objects.get_or_create(
                            medico=medico,
                            inicio=slot_start,
                            defaults={"fin": slot_end}
                        )
                        # Si se obtuvo un Turno existente, aseguramos que 'fin' este correcto
                        if not created_flag and turno.fin != slot_end:
                            turno.fin = slot_end
                            turno.save(update_fields=["fin"])
                        if created_flag:
                            created += 1
                except IntegrityError:
                    # Colisión rara; simplemente seguimos
                    pass

                slot_start = slot_end

        fecha = fecha + timedelta(days=1)

    return created
