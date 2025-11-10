from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def historia_clinica(request):
    return render(request, "historia_clinica/historia_clinica.html")

def lista_paciente(request):
    # pacientes = 
    # ctx = {
    #     "pacientes" : pacientes
    # }
    return render(request, "historia_clinica/lista_pacientes.html")