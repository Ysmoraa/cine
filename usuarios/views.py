from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroForm
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pelicula
from .forms import PeliculaForm
from .models import Horario, Silla, Sala, Reserva
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from datetime import datetime, timedelta



def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Guardamos sin confirmar
            usuario.set_password(form.cleaned_data["password1"])  # Encriptamos la contraseña
            usuario.save()  # Ahora sí guardamos

            messages.success(request, '✅ Usuario registrado correctamente. ¡Inicia sesión!')
            return redirect('login')  # Redirige al login
        else:
            messages.error(request, '❌ Error en el formulario. Revisa los campos.')
            print(form.errors)  # 🔴 Muestra los errores en la terminal para depuración

    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, "✅ Inicio de sesión exitoso.")
            return redirect('cartelera')  # Redirige a la cartelera o donde desees
        else:
            messages.error(request, "❌ Correo o contraseña incorrectos.")

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'usuarios/cartelera.html', {'peliculas': peliculas})
@login_required
def agregar_pelicula(request):
    if not request.user.is_staff:
        messages.error(request, '⚠️ No tienes permisos para agregar películas.')
        return redirect('cartelera')  # Ajusta la URL si es otra

    salas = Sala.objects.all()  # Obtener todas las salas

    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            tipo = request.POST.get('tipo')

            pelicula = form.save(commit=False)
            sala_id = request.POST.get("sala")
            if sala_id:
                pelicula.sala = Sala.objects.get(id_sala=sala_id)  # Se asigna la sala correctamente
            
            pelicula.sinopsis = request.POST.get('sinopsis')  # Captura la sinopsis desde el formulario

            if tipo == 'Estreno':
                pelicula.estreno = True
                pelicula.preventa = False
            elif tipo == 'Preventa':
                pelicula.estreno = False
                pelicula.preventa = True

            pelicula.save()
            messages.success(request, f'🎬 La película "{pelicula.titulo}" fue agregada exitosamente.')
            return redirect('agregar_pelicula')  # Ajusta la redirección si es necesario
        else:
            messages.error(request, '❌ Error al agregar la película. Revisa los campos.')

    else:
        form = PeliculaForm()

    return render(request, 'usuarios/agregar_pelicula.html', {'form': form, 'salas': salas})

def listar_horarios_disponibles(request):
    hoy = timezone.localtime(timezone.now()).date()
    horarios = Horario.objects.filter(fecha__gte=hoy).order_by("fecha", "hora")

    return render(request, "usuarios/listar_horario.html", {"horarios": horarios})

def detalle_pelicula(request, id_pelicula):
    pelicula = get_object_or_404(Pelicula, id_pelicula=id_pelicula)
    hoy = datetime.now().date()

    # Generar los próximos 7 días
    fechas_disponibles = [hoy + timedelta(days=i) for i in range(7)]

    # Filtrar horarios para los próximos 7 días
    horarios = Horario.objects.filter(pelicula=pelicula, fecha__range=(hoy, fechas_disponibles[-1])).order_by('fecha', 'hora')

    # Agrupar los horarios por fecha
    horarios_por_dia = {fecha: [] for fecha in fechas_disponibles}
    for horario in horarios:
        if horario.fecha in horarios_por_dia:
            horarios_por_dia[horario.fecha].append(horario)

    return render(request, 'usuarios/detalle_pelicula.html', {
        'pelicula': pelicula,
        'horarios_por_dia': horarios_por_dia
    })

def seleccionar_horario(request, id_pelicula):
    pelicula = get_object_or_404(Pelicula, id_pelicula=id_pelicula)
    horarios = Horario.objects.filter(pelicula=pelicula)
    if request.method == 'POST':
        horario_id = request.POST.get('horario_id')
        horario = get_object_or_404(Horario, id_horario=horario_id)
        # Aquí puedes redirigir a la compra o guardar la selección
        return render(request, 'usuarios/confirmacion.html', {'horario': horario})
    return render(request, 'usuarios/seleccionar_horario.html', {'pelicula': pelicula, 'horarios': horarios})

def seleccionar_sillas(request, horario_id):
    horario = get_object_or_404(Horario, id_horario=horario_id)
    sillas = Silla.objects.filter(sala=horario.sala)

    # Obtener las sillas reservadas solo para este horario
    sillas_ocupadas = Reserva.objects.filter(horario=horario).values_list('sillas__id_silla', flat=True)

    if request.method == 'POST':
        sillas_seleccionadas = request.POST.getlist('sillas')
        reserva = Reserva.objects.create(horario=horario, usuario=request.user)
        reserva.sillas.set(Silla.objects.filter(id_silla__in=sillas_seleccionadas))  # Asignar las sillas

        return redirect('confirmar_compra')

    return render(request, 'usuarios/seleccionar_sillas.html', {
        'horario': horario,
        'sillas': sillas,
        'sillas_ocupadas': list(sillas_ocupadas)  # Enviar la lista de IDs ocupados
    })

    return render(request, 'usuarios/seleccionar_sillas.html', {
        'horario': horario,
        'sillas': sillas,
        'sillas_ocupadas': list(sillas_ocupadas)  # Enviar la lista de IDs ocupados
    })
    
@receiver(post_save, sender=Sala)
def crear_sillas(sender, instance, created, **kwargs):
    if created:
        filas = int(instance.filas)  # Asegurar enteros
        columnas = int(instance.columnas)  # Asegurar enteros

        for fila in range(1, filas + 1):
            for columna in range(1, columnas + 1):
                Silla.objects.create(sala=instance, fila=fila, columna=columna)

@login_required
def reservar_sillas(request, horario_id):
    horario = get_object_or_404(Horario, id_horario=horario_id)

    if request.method == "POST":
        sillas_seleccionadas = request.POST.get("sillas", "").split(",")
        sillas_obj = Silla.objects.filter(id_silla__in=sillas_seleccionadas)

        # Verificar que ninguna silla esté ya reservada
        sillas_ocupadas = sillas_obj.filter(estado="ocupada")
        if sillas_ocupadas.exists():
            messages.error(request, "Algunas de las sillas seleccionadas ya están ocupadas.")
            return redirect("ver_sillas", horario_id=horario_id)

        # Crear la reserva
        reserva = Reserva.objects.create(usuario=request.user, horario=horario)
        reserva.sillas.set(sillas_obj)

        # Marcar las sillas como ocupadas
        sillas_obj.update(estado="ocupada")

        messages.success(request, "Reserva realizada con éxito.")
        return redirect("mis_reservas")  # Redirigir a la página de reservas del usuario

    return redirect("ver_sillas", horario_id=horario_id)

@login_required
def mis_reservas(request):
    if request.user.is_staff:
        reservas = Reserva.objects.all()  # Staff ve todas
    else:
        reservas = Reserva.objects.filter(usuario=request.user)  # Usuario solo las suyas
    
    return render(request, "usuarios/mis_reservas.html", {"reservas": reservas})

@user_passes_test(lambda u: u.is_staff)  # Solo staff puede acceder
def eliminar_pelicula(request, id_pelicula):
    pelicula = get_object_or_404(Pelicula, id_pelicula=id_pelicula)
    pelicula.delete()
    return redirect('cartelera')  # Reemplaza con el nombre correcto de tu URL de cartelera

@user_passes_test(lambda u: u.is_staff)  # Solo staff puede acceder
def crear_sala(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        tipo_sala = request.POST['tipo_sala']
        capacidad = int(request.POST['capacidad'])  # Convertir a entero
        filas = int(request.POST['filas'])  # Convertir a entero
        columnas = int(request.POST['columnas'])  # Convertir a entero

        # Crear y guardar la sala
        Sala.objects.create(
            nombre=nombre,
            tipo_sala=tipo_sala,
            capacidad=capacidad,
            filas=filas,
            columnas=columnas
        )

        return redirect('ver_salas')  # Redirigir a la lista de salas

    return render(request, 'usuarios/crear_sala.html')

@login_required
def ver_salas(request):
    if request.user.is_staff:
        salas = Sala.objects.all()  # Staff ve todas
    else:
        salas = Sala.objects.filter(usuario=request.user)  # Usuario solo las suyas
    
    return render(request, "usuarios/listar_salas.html", {"salas": salas})

@user_passes_test(lambda u: u.is_staff)  # Solo staff puede acceder
def eliminar_sala(request, id_sala):
    sala = get_object_or_404(Sala, id_sala=id_sala)
    sala.delete()
    return redirect('ver_salas')

@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo staff puede crear horarios
def crear_horarios(request):
    if request.method == 'POST':
        pelicula = Pelicula.objects.get(id_pelicula=request.POST['pelicula'])
        sala = Sala.objects.get(id_sala=request.POST['sala'])
        fecha = request.POST['fecha']
        hora = request.POST['hora']

        Horario.objects.create(pelicula=pelicula, sala=sala, fecha=fecha, hora=hora)
        return redirect('listar_horarios')

    peliculas = Pelicula.objects.all()
    salas = Sala.objects.all()
    return render(request, 'usuarios/crear_horario.html', {'peliculas': peliculas, 'salas': salas})


@login_required
def listar_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'usuarios/listar_horario.html', {'horarios': horarios})


@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo staff puede eliminar horarios
def eliminar_horarios(request, id_horario):
    horario = get_object_or_404(Horario, id_horario=id_horario)
    horario.delete()
    return redirect('listar_horarios')

@login_required
def eliminar_reservas(request, id_reserva):
    reserva = get_object_or_404(Reserva, id_reserva=id_reserva)
    reserva.delete()
    return redirect('mis_reservas')