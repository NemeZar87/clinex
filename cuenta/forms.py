from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioPersonalizado, HorarioTrabajo, LugarTrabajo
from django.utils import timezone

class CrearCuenta(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña'
        })
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["tipo_cuenta", "username", "first_name", "last_name", "fecha_nacimiento", "email", "telefono", "password1", "password2", "numero_dni", "foto_dni"]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Nombre completo'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Apellido completo'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                "type": "date",
                "max": timezone.localdate().isoformat()
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Correo electronico'
            }),
            'telefono': forms.NumberInput(attrs={
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);', # remplaza todos los caracteres que no sean numeros por nada y limita la cantidad de caracteres que puedes colocar a 11.
                'placeholder': 'Número de telefono'
            }),
            'numero_dni': forms.NumberInput(attrs={
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, '').slice(0,8);',
                'placeholder': 'Número de documento'
            }),
        }

class InicioSesion(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class HorarioTrabajoForm(forms.ModelForm):
    class Meta:
        model = HorarioTrabajo
        fields = ['lugar', 'dia', 'hora_inicio', 'hora_fin', 'tiempo_turno']
        widgets = {
            'hora_inicio': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
            'hora_fin': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
            'tiempo_turno': forms.TimeInput(
                format='%H:%M:%S',
                attrs={'type': 'time', 'step': 1, 'title': 'Duración entre turnos (HH:MM:SS)'}# 👈 muestra segundos
            ),
        }
    
    def __init__(self, *args, **kwargs):
        medico = kwargs.pop('medico', None)
        super().__init__(*args, **kwargs)
        if medico:
            self.fields['lugar'].queryset = medico.lugares.all()

class LugarTrabajoForm(forms.ModelForm):
    class Meta:
        model = LugarTrabajo
        fields = ['nombre', 'direccion', 'telefono']
        widgets = {
            'telefono' : forms.NumberInput(attrs={
                'oninput' : 'this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);' # remplaza todos los caracteres que no sean numeros por nada y limita la cantidad de caracteres que puedes colocar a 11.
            })
        }