from django import forms
from .models import Usuario
from .models import Pelicula
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    tipo_documento = forms.ChoiceField(
        choices=[
            ('TI', 'Tarjeta de Identidad'),
            ('CC', 'Cédula de Ciudadanía')
        ],
        required=True
    )
    genero = forms.ChoiceField(
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro')
        ],
        required=True
    )

    class Meta:
        model = Usuario
        fields = [
            'email', 'nombres', 'apellidos', 'direccion', 'telefono', 
            'fecha_nacimiento', 'ciudad', 'tipo_documento', 'genero', 
            'documento', 'password1', 'password2'  # ✅ Agregamos las contraseñas
        ]

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'imagen', 'genero', 'formato', 'sinopsis', 'estreno', 'preventa', 'trailer_url', 'calificacion']
