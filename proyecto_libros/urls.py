"""proyecto_libros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libros import views 

urlpatterns = [
    path('', views.mostrarIndex),
    path('login', views.iniciarSesion),
    path('logout', views.cerrarSesion),

    path('menu_admin', views.mostrarMenuAdmin),
    path('perfil_admin/<int:idusu>', views.mostrarPerfilAdmin),

    path('form_registrar_categoria', views.mostrarFormRegistrarcategoria),
    path('registrar_categoria', views.registrarCategoria),
    path('form_actualizar_categoria/<int:id>', views.mostrarFormActualizarcategoria),
    path('actualizar_categoria/<int:id>', views.actualizarcategoria),
    path('eliminar_categoria/<int:id>', views.eliminarcategoria),

    path('listar_historial', views.mostrarListarHistorial),

    path('menu_usuario', views.mostrarMenuUsuario),
    path('perfil_usuario/<int:idusu>', views.mostrarPerfilUsuario),
    path('listar_libros', views.mostrarListarLibros),

    path('form_registrar_libros', views.mostrarFormRegistrarlibros),
    path('registrar_libros', views.registrarlibros),
    path('form_actualizar_libros/<int:id>', views.mostrarFormActualizarlibros),
    path('actualizar_libros/<int:id>', views.actualizarlibros),
    path('eliminar_libros/<int:id>', views.eliminarlibros),

    path('form_registrar_prestamos', views.mostrarFormRegistrarPrestamos),
    path('registrar_prestamo', views.registrarprestamo),
    path('listar_prestamos', views.mostrarListarPrestamos),
    path('eliminar_prestamos/<int:id>', views.eliminarPrestamo),
    path('gesti_prestamos', views.mostrarGestiPrestamos),
    path('form_actualizar_prestamo/<int:id>', views.mostrarFormActualizarPrestamo),
    path('actualizar_prestamo/<int:id>', views.actualizarPrestamo),

    path('listar_usuarios', views.mostrarFormRegistrarUsuario),
    path('registrar_usuario',views.registrarUsuario),
    path('form_actualizar_usuario/<int:id>', views.mostrarFormActualizarUsuario),
    path('actualizar_usuario/<int:id>', views.actualizarUsuario),
    path('eliminar_usuario/<int:id>', views.eliminarUsuario),

    path('form_registrar_autor', views.mostrarFormRegistrarAutor),
    path('registrar_autor', views.registrarAutor),
    path('form_actualizar_autor/<int:id>', views.mostrarFormActualizarAutor),
    path('actualizar_autor/<int:id>', views.actualizarAutor),
    path('eliminar_autor/<int:id>', views.eliminarAutor),

    path('form_registrar_editorial', views.mostrarFormRegistrarEditorial),
    path('registrar_editorial', views.registrarEditorial),
    path('form_actualizar_editorial/<int:id>', views.mostrarFormActualizarEditorial),
    path('actualizar_editorial/<int:id>', views.actualizarEditorial),
    path('eliminar_editorial/<int:id>', views.eliminarEditorial),


]
