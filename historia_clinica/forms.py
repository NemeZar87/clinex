from django import forms
from .models import HistoriaClinica, Consulta



class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica

        exclude = ["usuario"]
        widgets = {
            'telefono' : forms.NumberInput(attrs={
                'oninput' : 'this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);' #gracias tomi, reutilice tu codigo.
            })
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta

        exclude = ["usuario", "profesional", "fecha"]