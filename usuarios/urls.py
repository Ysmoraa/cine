from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import agregar_pelicula,detalle_pelicula,seleccionar_sillas, reservar_sillas, mis_reservas,eliminar_pelicula, crear_sala, ver_salas, eliminar_sala, crear_horarios, listar_horarios, eliminar_horarios, eliminar_reservas
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('cartelera/', views.cartelera, name='cartelera'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('agregar_pelicula/', agregar_pelicula, name='agregar_pelicula'),
    path('seleccionar_horario/<int:id_pelicula>/', views.seleccionar_horario, name='seleccionar_horario'),
    path('pelicula/<int:id_pelicula>/', detalle_pelicula, name='detalle_pelicula'),
    path('horario/<int:horario_id>/sillas/', seleccionar_sillas, name='seleccionar_sillas'),
    path("horario/<int:horario_id>/reservar/", reservar_sillas, name="reservar_sillas"),
    path("mis-reservas/", mis_reservas, name="mis_reservas"),
    path('eliminar_pelicula/<int:id_pelicula>/', eliminar_pelicula, name='eliminar_pelicula'),
    path('crear_sala/', crear_sala, name='crear_sala'),
    path('ver_salas/', ver_salas, name='ver_salas'),
    path('eliminar_sala/<int:id_sala>/', eliminar_sala, name='eliminar_sala'),
    path('crear_horarios/', crear_horarios, name='crear_horarios'),
    path('listar_horarios/', listar_horarios, name='listar_horarios'),
    path('eliminar_horarios/<int:id_horario>/', eliminar_horarios, name='eliminar_horarios'),
    path('eliminar_reservas/<int:id_reserva>/', eliminar_reservas, name='eliminar_reservas'),
]