from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Sala, Pelicula, Horario, Reserva, Silla

Usuario = get_user_model()

class RegistroUsuarioTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registro_usuario(self):
        """Verifica que un usuario pueda registrarse con correo electrónico"""
        response = self.client.post(reverse('registro'), {
            'email': 'test@example.com',
            'password1': 'test12345',
            'password2': 'test12345',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'fecha_nacimiento': '1990-01-01',
            'tipo_documento': 'CC',
            'genero': 'M',
        })
        self.assertEqual(response.status_code, 302)  # Debe redirigir después del registro
        self.assertTrue(Usuario.objects.filter(email='test@example.com').exists())

class LoginUsuarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(email='usuario@example.com', password='test123')

    def test_login_usuario(self):
        """ Verifica que un usuario pueda iniciar sesión con su correo electrónico """
        login = self.client.login(email='usuario@example.com', password='test123')
        self.assertTrue(login)  # Debe devolver True si el login fue exitoso

        response = self.client.get(reverse('cartelera'))  # Página de inicio
        self.assertEqual(response.status_code, 200)

class CrearSalaTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = Usuario.objects.create_user(email='admin@example.com', password='test123', is_staff=True)

    def test_crear_sala_staff(self):
        """ Verifica que solo el staff pueda crear salas """
        self.client.login(email='admin@example.com', password='test123')
        response = self.client.post(reverse('crear_sala'), {
            'nombre': 'Sala 2',
            'tipo_sala': 'IMAX',
            'capacidad': 80,
            'filas': 8,
            'columnas': 10
        })
        self.assertEqual(response.status_code, 302)  # Redirige después de crear
        self.assertEqual(Sala.objects.count(), 1)  # Se asegura que la sala fue creada

class VerSalasTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear usuario administrador
        self.admin_user = Usuario.objects.create_user(
            email='admin@example.com', password='test123', is_staff=True  
        )

        # Crear una sala de prueba
        Sala.objects.create(nombre="Sala 1", tipo_sala="2D", capacidad=50, filas=5, columnas=10)

    def test_ver_salas(self):
        """ Verifica que solo los administradores puedan ver las salas """
        self.client.login(email='admin@example.com', password='test123')  # Iniciar sesión

        response = self.client.get(reverse('ver_salas'))  # Obtener la lista de salas

        self.assertEqual(response.status_code, 200)  # La respuesta debe ser exitosa
        self.assertContains(response, 'Sala 1')  # La sala debe estar en la respuesta

class CrearHorarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = Usuario.objects.create_user(email='admin@example.com', password='test123', is_staff=True)
        self.sala = Sala.objects.create(nombre="Sala 1", tipo_sala="2D", capacidad=50, filas=5, columnas=10)
        self.pelicula = Pelicula.objects.create(titulo="Pelicula Test", genero="Acción", formato="2D", calificacion=4)

    def test_crear_horario_staff(self):
        """ Verifica que solo el staff pueda crear horarios """
        self.client.login(email='admin@example.com', password='test123')
        response = self.client.post(reverse('crear_horarios'), {
            'pelicula': self.pelicula.id_pelicula,
            'sala': self.sala.id_sala,
            'fecha': "2025-04-05",
            'hora': "20:00"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Horario.objects.count(), 1)

class VerHorariosTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear usuario administrador
        self.admin_user = Usuario.objects.create_user(
            email='admin@example.com', password='test123', is_staff=True  
        )
        # Crear una sala y una película de prueba
        self.sala = Sala.objects.create(nombre="Sala 1", tipo_sala="2D", capacidad=50, filas=5, columnas=10)
        self.pelicula = Pelicula.objects.create(titulo="Pelicula Test", genero="Acción", formato="2D", calificacion=4)

        # Crear un horario de prueba
        Horario.objects.create(pelicula=self.pelicula, sala=self.sala, fecha="2025-04-02", hora="18:00")

    def test_ver_horarios_admin(self):
        """ Verifica que un usuario staff pueda ver los horarios """
        self.client.login(email='admin@example.com', password='test123')  # Iniciar sesión como admin

        response = self.client.get(reverse('listar_horarios'))  # Intentar acceder a los horarios

        self.assertEqual(response.status_code, 200)  # El admin debe poder ver los horarios
        self.assertContains(response, 'Pelicula Test')  # Verificar que la película aparece en la vista

class ReservarSillaTest(TestCase):  # 🔥 Asegúrate de que esté dentro de una clase que herede de TestCase
    def setUp(self):
        self.client = Client()

        # Crear usuario administrador
        self.admin_user = Usuario.objects.create_superuser(
            email="admin@example.com",
            password="admin123"
        )

        # Crear objetos necesarios
        self.sala = Sala.objects.create(nombre="Sala 1", tipo_sala="2D", capacidad=50)
        self.pelicula = Pelicula.objects.create(titulo="Dune", genero="Sci-Fi")
        self.horario = Horario.objects.create(
            sala=self.sala,
            pelicula=self.pelicula,
            fecha="2025-04-10",
            hora="18:00"
        )
        self.silla = Silla.objects.create(sala=self.sala, fila=1, columna=1)
        self.user = Usuario.objects.create_user(email="user@example.com", password="test123")

    def test_reservar_silla(self):  # 🚨 Este método DEBE estar dentro de la clase
        # Iniciar sesión como usuario normal
        self.client.login(email="user@example.com", password="test123")

        # Hacer la petición POST
        response = self.client.post(
            reverse('reservar_sillas', args=[self.horario.id_horario]),
            {
                'usuario': self.user.id_usuarios,
                'horario': self.horario.id_horario,
                'sillas': f"{self.silla.id_silla}"
            },
            follow=True
        )

        # Verificaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reserva.objects.count(), 1)  # ¿Se creó la reserva?