from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.db import models
from django.conf import settings


class UsuarioManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

TIPO_DOCUMENTO_CHOICES = [
    ('TI', 'Tarjeta de Identidad'),
    ('CC', 'Cédula de Ciudadanía')
]

GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro')
]

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuarios = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES, blank=True)  # ✅ Agregado
    genero = models.CharField(max_length=50, choices=GENERO_CHOICES, blank=True)  # ✅ Agregado
    documento = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='peliculas/')
    sinopsis = models.TextField(default="Sinopsis no disponible.")
    genero = models.CharField(max_length=100)
    formato = models.CharField(max_length=50)  # 2D, 3D, 4DX
    estreno = models.BooleanField(default=False)
    preventa = models.BooleanField(default=False)
    trailer_url = models.URLField()
    calificacion = models.IntegerField(default=0)  # de 1 a 5 estrellas

class Sala(models.Model):
    TIPO_SALA_CHOICES = [
        ('2D', '2D'),
        ('3D', '3D'),
        ('IMAX', 'IMAX'),
        ('VIP', 'VIP'),
    ]

    id_sala = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)  # Ejemplo: "Sala 1", "Sala VIP"
    tipo_sala = models.CharField(max_length=10, choices=TIPO_SALA_CHOICES, default='2D')
    capacidad = models.PositiveIntegerField(default=100)  # Asientos disponibles
    filas = models.PositiveIntegerField(default=10)  # Para la distribución visual
    columnas = models.PositiveIntegerField(default=10)  # Para la distribución visual

    def __str__(self):
        return f"{self.nombre} ({self.tipo_sala})"

class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name="horarios")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="horarios")
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.pelicula.titulo} - {self.sala.nombre} - {self.fecha} {self.hora}"


class Silla(models.Model):
    ESTADO_SILLA_CHOICES = [
        ('disponible', 'Disponible'),
        ('no-disponible', 'No disponible'),
        ('ocupada', 'Ocupada'),
    ]

    id_silla = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sillas')
    fila = models.PositiveIntegerField(default=10)  # Agregar este campo
    columna = models.PositiveIntegerField(default=10)  # Agregar este campo
    estado = models.CharField(max_length=15, choices=ESTADO_SILLA_CHOICES, default='disponible')

    def __str__(self):
        return f"Silla {self.fila}-{self.columna} en {self.sala.nombre}"

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas")
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name="reservas")
    sillas = models.ManyToManyField(Silla)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.get_username()} para {self.horario}"


