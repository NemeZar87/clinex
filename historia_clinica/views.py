from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from cuenta.models import Medico, UsuarioPersonalizado
from turno.models import Turno
from cuenta.services.servicios import medico_required
from .forms import HistoriaClinicaForm, ConsultaForm
from .models import HistoriaClinica, Consulta
from .repositories.conversor_hora import make_aware_if_needed



# Create your views here.

def mi_historia_clinica(request):
    try:
        historia = get_object_or_404(HistoriaClinica, usuario_id=request.user)
    except Http404:
        return HttpResponse("No se ha encontrado su historia clinica")

    consultas = Consulta.objects.filter(usuario_id=request.user).order_by('-fecha')

    ctx = {
        "historia": historia,
        "consultas": consultas,
    }

    return render(request, "historia_clinica/mi_historia.html", ctx)


@medico_required
def historia_clinica_view(request):
    medico = get_object_or_404(Medico, usuario=request.user)
    turnos_reservados = Turno.objects.filter(
        medico=medico,
        paciente_nombre__isnull=False
    ).order_by("inicio")
    lista_turnos_reservados = list(turnos_reservados)
    # print(lista_turnos_reservados)
    ctx = {
        "turnos": lista_turnos_reservados,
    }
    return render(request, "historia_clinica/historia_clinica.html", ctx)

@medico_required
def cargar_datos(request, paciente_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)
    historia = HistoriaClinica.objects.filter(usuario_id=paciente_id).first() #busca la primer coincidencia, Devulve None si no encuentra nada
    if request.method == "POST":
        form = HistoriaClinicaForm(request.POST, instance=historia)
        if form.is_valid():
            datos = form.save(commit=False)
            if historia is None:
                datos.usuario = paciente
            datos.save()
            return redirect('historia_clinica:detalle_paciente', paciente_id=paciente.id)
    else:
        form = HistoriaClinicaForm(instance=historia)

    ctx = {
        "form": form,
    }
    return render(request, "historia_clinica/cargar_datos.html", ctx)

@medico_required
def crear_consulta(request, paciente_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False) #guardamos los datos en un objeto pero no la bd
            consulta.usuario = paciente           # asignamos paciente
            consulta.profesional = request.user    # asignamos el usuario que crea la consulta (medico)
            consulta.save()
            return redirect('historia_clinica:detalle_paciente', paciente_id=paciente.id)
    else:
        form = ConsultaForm()
    
    return render(request, 'historia_clinica/crear_consulta.html', {'form': form, 'paciente': paciente})

def detalle_paciente(request, paciente_id):
    try:
        paciente = get_object_or_404(HistoriaClinica, usuario_id=paciente_id)
    except Http404:
        return HttpResponse("No se ha encontrado la historia clinica del paciente")
    consultas = Consulta.objects.filter(usuario_id=paciente_id, profesional=request.user).order_by('-fecha')

    ctx =  {
        'paciente': paciente,
        'consultas': consultas,
    }
    return render(request, 'historia_clinica/detalle_paciente.html', ctx)

def ver_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    fecha = make_aware_if_needed(consulta.fecha)
    ctx = {
        "consulta": consulta,
        "paciente": consulta.usuario,
        "fecha": fecha
    }
    return render(request, 'historia_clinica/ver_consulta.html', ctx)


def lista_paciente(request):
    # pacientes = 
    # ctx = {
    #     "pacientes" : pacientes
    # }
    return render(request, "historia_clinica/lista_pacientes.html")