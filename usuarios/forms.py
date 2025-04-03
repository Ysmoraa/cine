from django import forms
from .models import Usuario
from .models import Pelicula
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="❌ Ingresa un correo válido (ejemplo@ejemplo.com).")],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    nombres = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tus nombres'})
    )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tus apellidos'})
    )
    direccion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección'})
    )
    telefono = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d{10}$', message="❌ Ingresa un número de teléfono válido (10 dígitos).")],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'})
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ciudad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu ciudad'})
    )
    tipo_documento = forms.ChoiceField(
        choices=[
            ('TI', 'Tarjeta de Identidad'),
            ('CC', 'Cédula de Ciudadanía')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    genero = forms.ChoiceField(
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    documento = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        fields = [
            'email', 'nombres', 'apellidos', 'direccion', 'telefono', 
            'fecha_nacimiento', 'ciudad', 'tipo_documento', 'genero', 
            'documento', 'password1', 'password2'  # ✅ Se incluyen las contraseñas
        ]
        
class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'imagen', 'genero', 'formato', 'sinopsis', 'estreno', 'preventa', 'trailer_url', 'calificacion','sala']
