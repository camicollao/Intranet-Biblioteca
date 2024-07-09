from django.db import models

class Usuario(models.Model):
    rut_usuario = models.TextField(max_length=15)
    nombre_usuario = models.TextField(max_length=15)
    apellidop_usuario = models.TextField(max_length=15)
    apellidom_usuario = models.TextField(max_length=15)
    correo_usuario = models.TextField(max_length=30)
    telefono_usuario = models.TextField(max_length=15)
    password_usuario = models.TextField(max_length=20)
    direccion_usuario = models.TextField(max_length=30)
    fecha_nacimiento = models.DateTimeField()



class Categoria(models.Model):
   nombre_categoria = models.TextField(max_length=100)

class Editorial(models.Model):
   nombre_editorial = models.TextField(max_length=100)

class Autor(models.Model):
    nombre_autor = models.TextField(max_length=100)
    apellidop_autor = models.TextField(max_length=15)
    apellidom_autor = models.TextField(max_length=15)


class Libros(models.Model):
    numero_serie = models.TextField(max_length=10)
    titulo_libros = models.TextField(max_length=100)
    año_publicacion = models.TextField(max_length=4)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    
class Prestamos(models.Model):
    numero_orden = models.TextField(max_length=10)
    libro = models.ForeignKey(Libros, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField()
    fecha_devolucion=models.DateTimeField()
    #devolucion_real=models.DateTimeField()
    #dias_retraso = models.TextField(max_length=3)
    #multa = models.TextField(max_length=10)
    #costo_prestamo=models.TextField(max_length=10)
    #solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)




    


class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()

