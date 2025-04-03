from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Pelicula, Horario, Silla, Sala, Reserva

class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ('id_usuarios', 'email', 'nombres', 'apellidos', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'nombres')
    search_fields = ('email', 'nombres', 'apellidos')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'direccion', 'telefono', 'fecha_nacimiento', 'ciudad', 'tipo_documento', 'genero', 'documento')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombres', 'apellidos', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)

admin.site.register(Pelicula)

admin.site.register(Horario)

admin.site.register(Silla)

admin.site.register(Sala)

admin.site.register(Reserva)