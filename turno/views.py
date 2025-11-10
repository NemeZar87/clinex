from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from datetime import date, datetime, timedelta
from calendar import monthrange, monthcalendar, calendar
from .models import Turno
from cuenta.models import Medico, Paciente, HorarioTrabajo
from django.contrib.auth.decorators import login_required


@login_required
def crear_turno(request, year, month, day):
    # print("punto 0")
    medico_id = 2  # reemplazar por request.session.get("medico_id")
    horario_query = get_object_or_404(HorarioTrabajo, pk=medico_id)
    medico = horario_query.medico
    paciente = get_object_or_404(Paciente, usuario=request.user)
    fecha = date(year, month, day)
    # print("punto 1")

    # Generar turnos automáticamente si no existen
    # --- mapear weekday a texto con el formato de tus choices ---
    WEEKDAY_MAP = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo",
    }
    weekday_text = WEEKDAY_MAP[fecha.weekday()]
    ###
    # --- obtener todos los horarios del médico que sean para ese día ---
    horarios_validos = HorarioTrabajo.objects.filter(medico=medico, dia=weekday_text)

    # Si no hay horarios para ese día, devolvemos directamente (el template mostrará "no hay turnos")
    if not horarios_validos.exists():
        ctx = {"medico": medico, "fecha": fecha, "turnos": []}
        return render(request, "turno/crear_turno.html", ctx)


    # --- Generar turnos para cada horario válido (si no existen) ---
    ###

    # Obtener los turnos libres de ese día
    turnos_disponibles = Turno.objects.filter(
        medico=medico,
        inicio__date=fecha,
        paciente_nombre__isnull=True
    ).order_by("inicio")

    # print("punto 2")
    if request.method == "POST":
        turno_id = request.POST.get("turno_id")
        turno = get_object_or_404(Turno, id=turno_id)
        turno.paciente_nombre = paciente.usuario
        turno.save()
        return redirect("calendario")

    # print("punto 3")
    # print(medico)
    # print(horario_query)
    
    ctx = {"medico": medico,
        "fecha": fecha,
        "turnos": turnos_disponibles}
    
    return render(request, "turno/crear_turno.html", ctx)




def calendario(request):
    """
    Muestra el calendario del mes actual para un médico previamente seleccionado.
    Solo muestra turnos dentro del mes actual.
    """
    
    def generador_turno(fecha, medico_var, weekday_text):

        # --- helper para convertir a aware si es necesario ---
        def make_aware_if_needed(dt):
            if settings.USE_TZ:
                if timezone.is_naive(dt):
                    return timezone.make_aware(dt, timezone.get_default_timezone())
            return dt


        horarios_validos = HorarioTrabajo.objects.filter(medico=medico_var, dia=weekday_text)
        
        for horario in horarios_validos:
            inicio_dt = datetime.combine(fecha, horario.hora_inicio)
            fin_dt = datetime.combine(fecha, horario.hora_fin)
            inicio_dt = make_aware_if_needed(inicio_dt)
            fin_dt = make_aware_if_needed(fin_dt)
            intervalo = horario.tiempo_turno  # DurationField -> timedelta

            # protección: si tiempo_turno es 0 o negativo, saltar
            if not intervalo or intervalo.total_seconds() <= 0:
                continue

            # Generamos mientras que el turno completo entre dentro del intervalo
            current = inicio_dt
            while current + intervalo <= fin_dt:
                # Usamos get_or_create: buscamos por médico + inicio (fecha-hora)
                Turno.objects.get_or_create(
                    medico=medico_var,
                    inicio=current,
                    defaults={
                        "fin": current + intervalo,
                        "paciente_nombre": None
                    }
                )
                current += intervalo

    
    hoy = timezone.localdate()
    year = hoy.year
    month = hoy.month

    # Obtener el médico previamente seleccionado
    # print(f"Id del medico = {request.session.get("medico_id")}")
    medico_id = 2
    # medico_id = request.session.get("medico_id")  # o usar un ID fijo: medico_id = 1
    horario_query = get_object_or_404(HorarioTrabajo, pk=medico_id)
    medico_var = horario_query.medico
    
    dia_laboral = horario_query.dia
    hora_inicio = horario_query.hora_inicio
    hora_fin = horario_query.hora_fin

    # Calcular rango de fechas del mes
    _, dias_en_mes = monthrange(year, month)
    fecha_inicio = date(year, month, 1)
    fecha_fin = date(year, month, dias_en_mes)

    # Obtener los turnos del médico en el mes actual
    turnos_qs = Turno.objects.filter(
        medico=medico_var,
        inicio__date__gte=fecha_inicio,
        inicio__date__lte=fecha_fin
    ).select_related("medico")

    # Agrupar turnos por día
    turnos_por_dia = {}
    for t in turnos_qs:
        key = t.inicio.date()
        turnos_por_dia.setdefault(key, []).append(t)

    # Crear la estructura de semanas del mes
    WEEKDAY_MAP = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo",
    }

    semanas = monthcalendar(year, month)
    calendario = []

    for semana in semanas:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append({"date": None, "turnos": []})
            else:
                d = date(year, month, dia)
                weekday_text = WEEKDAY_MAP[d.weekday()]
                gen_turno = generador_turno(d, medico_var, weekday_text)
                dicc_temp = {
                    "date": d,
                    "turnos": sorted(turnos_por_dia.get(d, []), key=lambda x: x.inicio)
                }


    
                if weekday_text == dia_laboral:
                    #Verificamos si hay turnos libres en ese día
                    turno_libre= Turno.objects.filter(
                        medico=medico_var,
                        inicio__date=d,
                        paciente_nombre__isnull=True
                    ).exists()
                    #Ponemos el color que corresponda, dependiendo si hay turnos libres o no.
                    if turno_libre:
                        dicc_temp["color"] = "green"
                    else:
                        dicc_temp["color"] = "red"
                    dicc_temp["weekday"] = weekday_text
                #Si no es dia laborable, se pinta de gris.
                else:
                    dicc_temp["color"] = "gray"
                
                fila.append(dicc_temp)
        calendario.append(fila)
    
    # print(asd)
    # print(medico_var)
    # print(F"CALENDARIO: {calendario}")
    # print(dia_laboral)
    # print(hora_inicio)
    # print(hora_fin)
    # print(weekday_text)




        



    context = {
        "calendario": calendario,
        "dia": dia_laboral,       
        "inicio": hora_inicio,       
        "fin": hora_fin,       
        "year": year,
        "month": month,
        "medico": medico_var,
    }

    return render(request, "turno/calendario.html", context)

# Create your views here.
def turno(request):
    return render(request, "turno/turno.html")



#Falta que medico_id sea traido desde request (se lo mandariamos nosotros cuando el usuario clickea en el medico que desea ver sus horario.)
#Actualmente el programar esta puesto como version de prueba en id de medico = 2 pero es fijo, no sirve.
#atte: Chino (anotaciones mias)