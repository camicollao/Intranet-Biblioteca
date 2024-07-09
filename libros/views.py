from django.shortcuts import render
from libros.models import Prestamos, Usuario, Categoria, Libros, Historial, Autor, Editorial
from datetime import datetime
import random

#--------------------------------------------------------------------------------------------------------
def mostrarIndex(request):
    return render(request, 'index.html')


def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtusu"].upper()
        pas = request.POST["txtpas"]
        
        comprobarLogin = Usuario.objects.filter(nombre_usuario=nom, password_usuario=pas).values()
                
        if comprobarLogin:
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]["id"]
            request.session["nomUsuario"] = nom.upper()
            idusu = request.session["idUsuario"]
            
            datos = { 'nomUsuario' : nom.upper(), 'idUsuario' : comprobarLogin[0]["id"], "idusu" : idusu }
            
            des = "Inicia Sesión"
            tabla = ""
            fechayhora = datetime.now()
            usuario = request.session.get("idUsuario")
            his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
            his.save()
            
            if nom == "ADMIN":
                return render(request, 'menu_admin.html', datos)
            else:
                return render(request, 'menu_usuario.html', datos)
            
        else:
            
            datos = { "r2" : 'Error de Usuario y/o Contraseña!!'}
            return render(request, 'index.html', datos)
            
    else:

        datos = { "r2" : 'Debe Presionar el Boton del Formulario de Sesion!!'}
        return render(request, 'index.html', datos)



#--------------------------------------------------------------------------------------------------------



def cerrarSesion(request):
    try:
        idusu = request.session.get("idUsuario")
        del request.session["estadoSesion"]
        del request.session["idUsuario"]
        del request.session["nomUsuario"]
        
        des = "Cierra Sesión"
        tabla = ""
        fechayhora = datetime.now()
        usuario = idusu
        his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
        his.save()
        
        return render(request, "index.html")
    except:
        return render(request, "index.html")




#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------





def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario
        if nomUsuario == "ADMIN":
            datos = { 'nomUsuario' : nomUsuario, 'idusu' : idusu }
            return render(request, 'menu_admin.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------





def mostrarFormRegistrarcategoria(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            nomUsuario = request.session["nomUsuario"]
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario            
            cat =  Categoria.objects.all().values().order_by("nombre_categoria")            
            datos = { 'nomUsuario' : nomUsuario, 'cat' : cat, 'idusu' : idusu }
            return render(request, 'form_registrar_categoria.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)



#--------------------------------------------------------------------------------------------------------





def registrarCategoria(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            if request.method == "POST":
                
                nom = request.POST["txtest"].upper()
                comprobarcategoria = Categoria.objects.filter(nombre_categoria=nom)
                if comprobarcategoria:
                    #--- Si ya existe... se muestra error
                    cat = Categoria.objects.all().values().order_by("nombre_categoria")
                    datos = {
                                'r2' : 'la categoria Digitada Ya Existe!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'cat' : cat
                            }
                    return render(request, 'form_registrar_categoria.html', datos)
                else:
                    #--- Si NO existe... se procede a insertar.
                    cat = Categoria (nombre_categoria=nom)
                    cat.save()
                    
                    #--- Se registra en la tabla historial la nueva inserción realizada.
                    des = "Insert Realizado ("+str(nom)+")"
                    tabla = "categoria"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()
                    
                    cat = Categoria.objects.all().values().order_by("nombre_categoria")
                    datos = {
                                'r' : 'categoria ('+str(nom)+') Registrado Correctamente!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'cat' : cat
                            }
                    return render(request, 'form_registrar_categoria.html', datos)
                    
            else:
                cat = Categoria.objects.all().values().order_by("nombre_categoria")
                datos = {
                            'r2' : 'Debe Presionar El Boton del Formulario De categoria!!',
                            'nomUsuario' : request.session["nomUsuario"], 
                            'cat' : cat
                        }
                return render(request, 'form_registrar_categoria.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------





def mostrarFormActualizarcategoria(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            
            nomUsuario = request.session.get("nomUsuario")
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario   

            if nomUsuario == "ADMIN":                               
                
                encontrado = Categoria.objects.get(id=id)

                cat = Categoria.objects.all().values().order_by("nombre_categoria")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'cat' : cat,
                    'idusu' : idusu
                }

                return render(request, 'form_actualizar_categoria.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
                return render(request, 'index.html', datos)
            
        else:

            datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:

        cat = Categoria.objects.all().values().order_by("nombre_categoria")

        datos = { 
            'nomUsuario' : request.session["nomUsuario"],
            'cat':cat,
            'r2':"El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
        }

        return render(request, 'form_registrar_categoria.html', datos)





#--------------------------------------------------------------------------------------------------------





def actualizarcategoria(request, id):

    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":         



            try:
                nom = request.POST['txtest'].upper()

                cat = Categoria.objects.get(id=id)
                cat.nombre_categoria = nom
                cat.save()


                # se registra en la tabla historial.
                descripcion = "Actualización realizada ("+nom.lower()+")"
                tabla = "categoria"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()


                cat = Categoria.objects.all().values().order_by("nombre_categoria")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'cat' : cat, 
                    'r':"Datos Modificados Correctamente!!"         
                }

                return render(request, 'form_registrar_categoria.html', datos)

            except:
    
                cat = Categoria.objects.all().values().order_by("nombre_categoria")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'cat' : cat,
                    'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
                }

                return render(request, 'form_registrar_categoria.html', datos)

        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
        
    else:

        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------





def eliminarcategoria(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            try:
                cat = Categoria.objects.get(id=id)
                nom = cat.nombre_categoria
                cat.delete()
                
                #--- Se registra en la tabla historial la nueva inserción realizada.
                des = "Eliminación Realizada ("+str(nom)+")"
                tabla = "categoria"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                his.save()
                
                cat = Categoria.objects.all().values().order_by("nombre_categoria")
                datos = { 
                         'r' : 'Registro '+nom+" Eliminado Correctamente!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'cat' : cat
                        }
                return render(request, 'form_registrar_categoria.html', datos)
                
            except:
                cat = Categoria.objects.all().values().order_by("nombre_categoria")
                datos = { 
                         'r2' : 'El ID '+str(id)+" No Existe. Imposible Eliminar!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'cat' : cat
                        }
                return render(request, 'form_registrar_categoria.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------





def mostrarListarHistorial(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario == "ADMIN":
            his = Historial.objects.select_related("usuario").all().order_by("-fecha_hora_historial")
            datos = { 'nomUsuario' : nomUsuario, 'his' : his, 'idusu' : idusu }
            return render(request, 'listar_historial.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------





def mostrarMenuUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario != "ADMIN":
            datos = { 'nomUsuario' : nomUsuario, 'idusu' : idusu }
            return render(request, 'menu_usuario.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Usuario!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------





def eliminarlibros(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            
            try:
                lib = Libros.objects.get(id = id)
                nom = lib.titulo_libros.upper()
                lib.delete()
                
                
                des = "Eliminación Realizada ("+str(nom)+")"
                tabla = "libros"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                his.save()
                
                
                lib = Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                datos = { "nomUsuario" : request.session["nomUsuario"], "lib" : lib, 'r' : 'libros ('+str(nom)+') Eliminada Correctamente!!'}
                return render(request, 'form_registrar_libros.html', datos)
                
            except:
                lib = Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                datos = { "nomUsuario" : request.session["nomUsuario"], "lib" : lib, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!'}
                return render(request, 'form_registrar_libros.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------





def mostrarFormRegistrarlibros(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario == "ADMIN":
            lib = Libros.objects.select_related("categoria").all().order_by("id")
            opcionescategoria = Categoria.objects.all().values().order_by("nombre_categoria")
            opcionesautor = Autor.objects.all().values().order_by("nombre_autor")
            opcioneseditorial = Editorial.objects.all().values().order_by("nombre_editorial")
            datos = { 'nomUsuario' : nomUsuario, 'lib' : lib, 'opcionescategoria' : opcionescategoria, 'opcionesautor' : opcionesautor, 'opcioneseditorial' : opcioneseditorial, 'idusu' : idusu }
            return render(request, 'form_registrar_libros.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)






#--------------------------------------------------------------------------------------------------------





def registrarlibros(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            
            if request.method == "POST":
                aleatorio = random.randint(0, 9999)
                numero = str(aleatorio)
                tit = request.POST["txttit"]
                cat = request.POST["cbocat"]
                art = request.POST["cboart"]
                edi = request.POST["cboedi"]
                publi = request.POST["txtpubli"]
                
                comprobarTitulo = Libros.objects.filter(titulo_libros=tit)
                if comprobarTitulo:
                    opcionescategoria = Categoria.objects.all().values().order_by("nombre_categoria")
                    opcionesautor = Autor.objects.all().values().order_by("nombre_autor")
                    opcioneseditorial = Editorial.objects.all().values().order_by("nombre_editorial")
                    lib = Libros.objects.select_related("categoria").all().order_by("id")


                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'opcionescategoria' : opcionescategoria,
                        'opcionesautor' : opcionesautor,
                        'opcioneseditorial' : opcioneseditorial,
                        'lib' : lib,

                        'r2' : 'El Titulo ('+str(tit.upper())+') Ya Existe!!'
                    }
                    return render(request, "form_registrar_libros.html", datos)
                
                else:
                    lib = Libros(numero_serie=numero, titulo_libros=tit, año_publicacion= str(publi), categoria_id=cat, autor_id=art, editorial_id = edi)
                    lib.save()
                    
                    opcionescategoria = Categoria.objects.all().values().order_by("nombre_categoria")
                    opcionesautor = Autor.objects.all().values().order_by("nombre_autor")
                    opcioneseditorial = Editorial.objects.all().values().order_by("nombre_editorial")
                    lib = Libros.objects.select_related("categoria").all().order_by("id")

                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'opcionescategoria' : opcionescategoria,
                        'opcionesautor' : opcionesautor,
                        'opcioneseditorial' : opcioneseditorial,
                        'lib' : lib,

                        'r' : 'libros ('+str(tit.upper())+') Registrada Correctamente!!'
                    }
                    return render(request, "form_registrar_libros.html", datos)
            
            else:
                
                opcionescategoria = Categoria.objects.all().values().order_by("nombre_categoria")
                opcionesautor = Autor.objects.all().values().order_by("nombre_autor")
                opcioneseditorial = Editorial.objects.all().values().order_by("nombre_editorial")
                lib = Libros.objects.select_related("categoria").all().order_by("id")
                

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'opcionescategoria' : opcionescategoria,
                    'opcionesautor' : opcionesautor,
                    'opcioneseditorial' : opcioneseditorial,
                    'lib' : lib,

                    'r2' : 'No Se Puede Procesar La Solicitud!!'
                }
                return render(request, "form_registrar_libros.html", datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)






#--------------------------------------------------------------------------------------------------------





def mostrarFormActualizarlibros(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario == "ADMIN":
            
            try:
                encontrado = Libros.objects.get(id = id)
                opcionescategoria = Categoria.objects.all().values().order_by("nombre_categoria")
                opcionesautor = Autor.objects.all().values().order_by("nombre_autor")
                opcioneseditorial = Editorial.objects.all().values().order_by("nombre_editorial")

                datos = { 'encontrado' : encontrado, 'nomUsuario' : nomUsuario, 'opcionescategoria' : opcionescategoria,'opcionesautor' : opcionesautor,'opcioneseditorial' : opcioneseditorial, 'idusu' : idusu }
                return render(request, 'form_actualizar_libros.html', datos)
            except:
                lib =   Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                datos = { "nomUsuario" : nomUsuario, "lib" : lib, 'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar Datos!!" }
                return render(request, "form_registrar_libros.html", datos)

                
                
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------



def actualizarlibros(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            
            if request.method == "POST":
                tit = request.POST["txttit"]
                cat = request.POST["cbocat"]
                art = request.POST["cboart"]
                edi = request.POST["cboedi"]
                publi = request.POST["txtpubli"]

                try:
                    lib = Libros.objects.get(id = id)
                    lib.titulo_libros = tit
                    lib.categoria_id = cat
                    lib.autor_id = art
                    lib.editorial_id = edi
                    lib.año_publicacion = str(publi)
                    lib.save()
                    
                    des = "Actualización Realizada ("+str(id)+")"
                    tabla = "libros"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()
                    
                    lib = Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'lib' : lib, 'r' : 'Datos Actualizados Correctamente!!' }
                    return render(request, "form_registrar_libros.html", datos)
                    
                except:
                    lib = Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'lib' : lib, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar Datos!!' }
                    return render(request, "form_registrar_libros.html", datos)
                
            else:
                lib = Libros.objects.select_related("categoria").all().order_by("titulo_libros")
                datos = { 'nomUsuario' : request.session["nomUsuario"], 'lib' : lib, 'r2' : 'Error al Procesar Solicitud!!' }
                return render(request, "form_registrar_libros.html", datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------

def registrarprestamo(request):
    estado_sesion = request.session.get("estadoSesion")

    if estado_sesion is True:
        if request.method == "POST":
            aleatorio = random.randint(0, 9999)
            numero = str(aleatorio)
            libro = request.POST["cbolib"]
            fecha_prestamo = datetime.now()
            fecha_devolucion = request.POST["fecha_devolucion"]

            # Registro
            prestamo = Prestamos(numero_orden=numero, libro_id=libro, fecha_prestamo=fecha_prestamo, fecha_devolucion=fecha_devolucion)
            prestamo.save()

            # Registro historial
            descripcion = "Prestamo realizado - Fecha de devolución: {fecha_devolucion}"
            tabla_afectada = "prestamo"
            fecha_hora = datetime.now()
            usuario = request.session["idUsuario"]

            historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla_afectada, fecha_hora_historial=fecha_hora, usuario_id=usuario)
            historial.save()



            prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
            opcioneslibros = Libros.objects.all().values().order_by("titulo_libros")
            datos = {'prestamo' : prestamos, 'opcioneslibros' : opcioneslibros,
                'mensaje': 'Préstamo de {libro} registrado correctamente.',
                'nomUsuario': request.session["nomUsuario"],
            }

            return render(request, 'listar_prestamos.html', datos)
        else:
            datos = {
                'mensaje': 'Debe enviar el formulario de préstamo.',
                'nomUsuario': request.session["nomUsuario"],
            }
            return render(request, 'realizar_prestamo.html', datos)
    else:
        datos = {'mensaje': 'Debe iniciar sesión para acceder.',}
        return render(request, 'index.html', datos)
    

#-----------------------------------------------------------------------------------------

def mostrarFormRegistrarPrestamos(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario != "ADMIN":
            opcioneslibros = Libros.objects.all().values().order_by("titulo_libros")
            datos = { 'nomUsuario': request.session["nomUsuario"], 'opcioneslibros' : opcioneslibros, 'idusu' :idusu }
            return render(request, 'form_registrar_prestamos.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
#-------------------------------------------------------------------------------


def eliminarPrestamo(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:            
        try:
            pres = Prestamos.objects.get(id = id)
            pres.delete()
            
            
            des = "Eliminación Realizada"
            tabla = "Prestamos"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
            his.save()
            
            prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
            datos = { "nomUsuario" : request.session["nomUsuario"], "prestamo" : prestamos, 'r' : 'Prestamo cancelado correctamente!!'}
            return render(request, 'listar_prestamos.html', datos)
            
        except:
            prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
            datos = { "nomUsuario" : request.session["nomUsuario"], "prestamo" : prestamos, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!'}
            return render(request, 'listar_prestamos.html', datos)
            
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
    
#-------------------------------------------------------------------------------

    
def mostrarListarPrestamos(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario != "ADMIN":
            prestamos = Prestamos.objects.all().order_by("id")
            opcioneslibros = Libros.objects.select_related("categoria").all().values().order_by("id")
            opcionescategoria = Categoria.objects.all().values().order_by("id")
            opcionesautor = Autor.objects.all().values().order_by("id")
            opcioneseditorial = Editorial.objects.all().values().order_by("id")
            datos = {'nomUsuario': request.session["nomUsuario"], 'prestamo' : prestamos, 'opcioneslibros' : opcioneslibros, 'opcionescategoria' : opcionescategoria, 'opcionesautor' : opcionesautor, 'opcioneseditorial' : opcioneseditorial, 'idusu' : idusu }
            return render(request, 'listar_prestamos.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#-------------------------------------------------------------------------------
    
def mostrarListarLibros(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario != "ADMIN":
            lib = Libros.objects.select_related("categoria").all().order_by("id")
            datos = {'nomUsuario': request.session["nomUsuario"], 'prestamo' : lib, 'lib' : lib, 'idusu' : idusu }
            return render(request, 'listar_libros.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#-------------------------------------------------------------------------------


def mostrarGestiPrestamos(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario == "ADMIN":
            prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
            opcioneslibros = Libros.objects.all().values().order_by("titulo_libros")
            datos = {'nomUsuario': request.session["nomUsuario"], 'prestamos' : prestamos, 'opcioneslibros' : opcioneslibros, 'idusu' : idusu }
            return render(request, 'gesti_prestamos.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
    


#--------------------------------------------------------------------------------------------------------





def mostrarFormActualizarPrestamo(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        idUsuario = request.session.get("idUsuario")
        idusu = idUsuario   
        if nomUsuario == "ADMIN":
            try:
                encontrado = Prestamos.objects.get(id = id)
                opcioneslibros = Libros.objects.all().values().order_by("id")
                datos = { 'encontrado' : encontrado, 'nomUsuario' : nomUsuario, 'opcioneslibros' : opcioneslibros, 'idusu' : idusu}
                return render(request, 'form_actualizar_prestamo.html', datos)
            except:
                prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
                datos = { "nomUsuario" : nomUsuario, "prestamos" : prestamos, 'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar Datos!!" }
                return render(request, "gesti_prestamos.html", datos)

        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)





#--------------------------------------------------------------------------------------------------------



def actualizarPrestamo(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            if request.method == "POST":
                    
                lib = request.POST["cbolib"]
                devo = request.POST["fecha_devolucion"]
                try:

                    pre = Prestamos.objects.get(id = id)
                    pre.libros_id = lib
                    pre.fecha_devolucion = devo
                    pre.save()
                    
                    prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'prestamos' : prestamos, 'r' : 'Datos Actualizados Correctamente!!' }
                    return render(request, "gesti_prestamos.html", datos)
                    
                except:
                    prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'prestamos' : prestamos, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar Datos!!' }
                    return render(request, "gesti_prestamos.html", datos)

            else:
                prestamos = Prestamos.objects.select_related('libro').all().order_by("id")
                datos = { 'nomUsuario' : request.session["nomUsuario"], 'prestamos' : prestamos, 'r2' : 'Error al Procesar Solicitud!!' }
                return render(request, "gesti_prestamos.html", datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)



#-------------------------------------------------------------------------------

def mostrarFormRegistrarUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            nomUsuario = request.session["nomUsuario"]        
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario       
            usu =  Usuario.objects.all().values().order_by("nombre_usuario")            
            datos = { 'nomUsuario' : nomUsuario, 'usu' : usu, 'idusu' : idusu }
            return render(request, 'listar_usuarios.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#-------------------------------------------------------------------------------

def registrarUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            if request.method == "POST":
                
                rut = request.POST["txtrut"]
                nom = request.POST["txtusu"].upper()
                apep = request.POST["txtapep"].upper()
                apem = request.POST["txtapem"].upper()
                cor = request.POST["txtcor"].upper()
                tel = request.POST["txttel"]
                direc = request.POST["txtdirec"].upper()
                fecna = request.POST["fecna"]
                pas = request.POST["txtpas"]
                comprobarusuario = Usuario.objects.filter(nombre_usuario=nom)
                if comprobarusuario:
                    usu = Usuario.objects.all().values().order_by("nombre_usuario")
                    datos = {
                                'r2' : 'Ya Existe un usuario con ese nombre de usuario',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'usu' : usu
                            }
                    return render(request, 'listar_usuarios.html', datos)
                else:
                    usu = Usuario ( rut_usuario = rut, nombre_usuario=nom, apellidop_usuario = apep, apellidom_usuario = apem, correo_usuario = cor, telefono_usuario = tel, direccion_usuario=direc, fecha_nacimiento=fecna,  password_usuario=pas)
                    usu.save()
                    
                    des = "Insert Realizado ("+str(nom)+")"
                    tabla = "Usuario"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()

                    usu = Usuario.objects.all().values().order_by("id")
                    datos = {
                                'r' : 'Usuario ('+str(nom)+') Registrado Correctamente!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'usu' : usu
                            }
                    return render(request, 'listar_usuarios.html', datos)
                    
            else:
                usu = Usuario.objects.all().values().order_by("id")
                datos = {
                            'r2' : 'Debe Presionar El Boton del Formulario De Usuarios!!',
                            'nomUsuario' : request.session["nomUsuario"], 
                            'usu' : usu
                        }
                return render(request, 'listar_usuarios.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#-------------------------------------------------------------------------------

def mostrarFormActualizarUsuario(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session["nomUsuario"]
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario           
            if request.session["nomUsuario"].upper() == "ADMIN":
                    
                usuencontrado = Usuario.objects.get(id=id)    
                usu =  Usuario.objects.all().values().order_by("nombre_usuario")          

                datos = { 'usuencontrado' : usuencontrado, 'nomUsuario' : nomUsuario, 'usu' : usu, 'idusu' : idusu}
                return render(request, 'form_actualizar_usuario.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
            usu = Usuario.objects.all().values().order_by("nombre_usuario")
            datos = { "nomUsuario" : nomUsuario, "usu" : usu, 'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar Datos!!" }
            return render(request, 'listar_usuarios.html', datos)


#-------------------------------------------------------------------------------
def actualizarUsuario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            
            if request.method == "POST":

                rut = request.POST["txtrut"]
                nom = request.POST["txtusu"].upper()
                apep = request.POST["txtapep"].upper()
                apem = request.POST["txtapem"].upper()
                cor = request.POST["txtcor"].upper()
                tel = request.POST["txttel"]
                pas = request.POST["txtpas"]
                direc = request.POST["txtdirec"].upper()
                fecna = request.POST["fecna"]
                
                try:
                    usu = Usuario.objects.get(id = id)
                    usu.rut_usuario = rut
                    usu.nombre_usuario = nom
                    usu.apellidop_usuario = apep
                    usu.apellidom_usuario = apem
                    usu.correo_usuario = cor
                    usu.telefono_usuario = tel
                    usu.direccion_usuario = direc
                    usu.fecha_nacimiento = fecna
                    usu.password_usuario = pas
                    usu.save()
                    
                    des = "Actualización Realizada ("+str(id)+")"
                    tabla = "Usuario"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()
                    
                    usu =  Usuario.objects.all().values().order_by("id")       
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'usu' : usu, 'r' : 'Datos Actualizados Correctamente!!' }
                    return render(request, 'listar_usuarios.html', datos)
                    
                except:
                    usu =  Usuario.objects.all().values().order_by("id")       
                    datos = { 'nomUsuario' : request.session["nomUsuario"], 'usu' : usu, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar Datos!!' }
                    return render(request, 'listar_usuarios.html', datos)
                
            else:
                usu =  Usuario.objects.all().values().order_by("id")       
                datos = { 'nomUsuario' : request.session["nomUsuario"], 'usu' : usu, 'r2' : 'Error al Procesar Solicitud!!' }
                return render(request, 'listar_usuarios.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#-------------------------------------------------------------------------------
def eliminarUsuario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            try:
                usu = Usuario.objects.get(id = id)
                usu.delete()
                
                
                des = "Eliminación Realizada"
                tabla = "Usuario"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                his.save()
                
                usu =  Usuario.objects.all().values().order_by("nombre_usuario")       
                datos = { "nomUsuario" : request.session["nomUsuario"], "usu" : usu, 'r' : 'Usuario eliminado correctamente!!'}
                return render(request, 'listar_usuarios.html', datos)
                
            except:
                usu =  Usuario.objects.all().values().order_by("nombre_usuario")       
                datos = { "nomUsuario" : request.session["nomUsuario"], "usu" : usu, 'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!'}
                return render(request, 'listar_usuarios.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#-------------------------------------------------------------------------------
def mostrarFormRegistrarAutor(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            nomUsuario = request.session["nomUsuario"]
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario     
          
            art =  Autor.objects.all().values().order_by("nombre_autor")            
            datos = { 'nomUsuario' : nomUsuario, 'art' : art, 'idusu' : idusu }
            return render(request, 'form_registrar_autor.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)
#--------------------------------------------------------------------------------------------------------
def registrarAutor(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            if request.method == "POST":
                
                nom = request.POST["txtest"].upper()
                apep = request.POST["txtapep"].upper()
                apem = request.POST["txtapem"].upper()

                comprobarautor = Autor.objects.filter(nombre_autor=nom)
                if comprobarautor:
                    art = Autor.objects.all().values().order_by("id")
                    datos = {
                                'r2' : 'El Autor Digitado Ya Existe!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'art' : art
                            }
                    return render(request, 'form_registrar_autor.html', datos)
                else:
                    #--- Si NO existe... se procede a insertar.
                    art = Autor (nombre_autor=nom, apellidop_autor=apep, apellidom_autor=apem)
                    art.save()
                    
                    #--- Se registra en la tabla historial la nueva inserción realizada.
                    des = "Insert Realizado ("+str(nom)+")"
                    tabla = "Autores"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()
                    
                    art = Autor.objects.all().values().order_by("id")
                    datos = {
                                'r' : 'El autor ('+str(nom)+') Registrado Correctamente!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'art' : art
                            }
                    return render(request, 'form_registrar_autor.html', datos)
                    
            else:
                art = Autor.objects.all().values().order_by("nombre_autor")
                datos = {
                            'r2' : 'Debe Presionar El Boton del Formulario De categoria!!',
                            'nomUsuario' : request.session["nomUsuario"], 
                            'art' : art
                        }
                return render(request, 'form_registrar_autor.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#--------------------------------------------------------------------------------------------------------
def mostrarFormActualizarAutor(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            
            nomUsuario = request.session.get("nomUsuario")
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario   
            if nomUsuario == "ADMIN":                               
                
                encontrado = Autor.objects.get(id=id)

                art = Autor.objects.all().values().order_by("nombre_autor")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'art' : art,
                    'idusu' : idusu
                }

                return render(request, 'form_actualizar_autor.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
                return render(request, 'index.html', datos)
            
        else:

            datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:

        art = Autor.objects.all().values().order_by("nombre_autor")

        datos = { 
            'nomUsuario' : request.session["nomUsuario"],
            'art': art,
            'r2':"El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
        }

        return render(request, 'form_registrar_autor.html', datos)

#--------------------------------------------------------------------------------------------------------
def actualizarAutor(request, id):

    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":         

            try:
                nom = request.POST['txtest'].upper()
                apep = request.POST["txtapep"].upper()
                apem = request.POST["txtapem"].upper()

                art = Autor.objects.get(id=id)
                art.nombre_autor = nom
                art.apellidop_autor = apep
                art.apellidom_autor = apem
                art.save()


                # se registra en la tabla historial.
                descripcion = "Actualización realizada ("+nom.lower()+")"
                tabla = "Autores"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()


                art = Autor.objects.all().values().order_by("nombre_autor")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'art' : art, 
                    'r':"Datos Modificados Correctamente!!"         
                }

                return render(request, 'form_registrar_autor.html', datos)

            except:
    
                art = Autor.objects.all().values().order_by("nombre_autor")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'art' : art,
                    'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
                }

                return render(request, 'form_registrar_autor.html', datos)

        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
        
    else:

        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#--------------------------------------------------------------------------------------------------------
def eliminarAutor(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            try:
                art = Autor.objects.get(id=id)
                nom = art.nombre_autor
                art.delete()
                
                #--- Se registra en la tabla historial la nueva inserción realizada.
                des = "Eliminación Realizada ("+str(nom)+")"
                tabla = "Autores"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                his.save()
                
                art = Autor.objects.all().values().order_by("nombre_autor")
                datos = { 
                         'r' : 'Registro '+nom+" Eliminado Correctamente!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'art' : art
                        }
                return render(request, 'form_registrar_autor.html', datos)
                
            except:
                art = Autor.objects.all().values().order_by("nombre_autor")
                datos = { 
                         'r2' : 'El ID '+str(id)+" No Existe. Imposible Eliminar!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'art' : art
                        }
                return render(request, 'form_registrar_autor.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#--------------------------------------------------------------------------------------------------------
def mostrarFormRegistrarEditorial(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            nomUsuario = request.session["nomUsuario"]    
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario           
            edi =  Editorial.objects.all().values().order_by("nombre_editorial")            
            datos = { 'nomUsuario' : nomUsuario, 'edi' : edi, 'idusu' : idusu }
            return render(request, 'form_registrar_editorial.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#--------------------------------------------------------------------------------------------------------
def registrarEditorial(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            if request.method == "POST":
                
                nom = request.POST["txtest"].upper()
                comprobarautor = Editorial.objects.filter(nombre_editorial=nom)
                if comprobarautor:
                    edi = Editorial.objects.all().values().order_by("nombre_editorial")
                    datos = {
                                'r2' : 'La Editorial Digitada Ya Existe!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'edi' : edi
                            }
                    return render(request, 'form_registrar_editorial.html', datos)
                else:
                    #--- Si NO existe... se procede a insertar.
                    edi = Editorial (nombre_editorial=nom)
                    edi.save()
                    
                    #--- Se registra en la tabla historial la nueva inserción realizada.
                    des = "Insert Realizado ("+str(nom)+")"
                    tabla = "Editoriales"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                    his.save()
                    
                    edi = Editorial.objects.all().values().order_by("nombre_editorial")
                    datos = {
                                'r' : 'El autor ('+str(nom)+') Registrado Correctamente!!',
                                'nomUsuario' : request.session["nomUsuario"], 
                                'edi' : edi
                            }
                    return render(request, 'form_registrar_editorial.html', datos)
                    
            else:
                edi = Editorial.objects.all().values().order_by("nombre_editorial")
                datos = {
                            'r2' : 'Debe Presionar El Boton del Formulario De categoria!!',
                            'nomUsuario' : request.session["nomUsuario"], 
                            'edi' : edi
                        }
                return render(request, 'form_registrar_editorial.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#--------------------------------------------------------------------------------------------------------

def mostrarFormActualizarEditorial(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            
            nomUsuario = request.session.get("nomUsuario")
            idUsuario = request.session.get("idUsuario")
            idusu = idUsuario   
            if nomUsuario == "ADMIN":                               
                
                encontrado = Editorial.objects.get(id=id)

                edi = Editorial.objects.all().values().order_by("nombre_editorial")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'edi' : edi,
                    'idusu' : idusu
                }

                return render(request, 'form_actualizar_editorial.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
                return render(request, 'index.html', datos)
            
        else:

            datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:

        edi = Editorial.objects.all().values().order_by("nombre_editorial")

        datos = { 
            'nomUsuario' : request.session["nomUsuario"],
            'edi' : edi,
            'r2':"El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
        }

        return render(request, 'form_registrar_editorial.html', datos)

#--------------------------------------------------------------------------------------------------------
def actualizarEditorial(request, id):

    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":         

            try:
                nom = request.POST['txtest'].upper()

                edi = Editorial.objects.get(id=id)
                edi.nombre_editorial = nom
                edi.save()


                # se registra en la tabla historial.
                descripcion = "Actualización realizada ("+nom.lower()+")"
                tabla = "Editoriales"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()


                edi = Editorial.objects.all().values().order_by("nombre_editorial")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'edi' : edi, 
                    'r':"Datos Modificados Correctamente!!"         
                }

                return render(request, 'form_registrar_editorial.html', datos)

            except:
    
                edi = Editorial.objects.all().values().order_by("nombre_editorial")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'edi' : edi,
                    'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar!!"         
                }

                return render(request, 'form_registrar_editorial.html', datos)

        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
        
    else:

        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)



#--------------------------------------------------------------------------------------------------------

def eliminarEditorial(request, id):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":
            
            try:
                edi = Editorial.objects.get(id=id)
                nom = edi.nombre_editorial
                edi.delete()
                
                #--- Se registra en la tabla historial la nueva inserción realizada.
                des = "Eliminación Realizada ("+str(nom)+")"
                tabla = "Editoriales"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=des,  tabla_afectada_historial=tabla,  fecha_hora_historial=fechayhora,  usuario_id=usuario)
                his.save()
                
                edi = Editorial.objects.all().values().order_by("nombre_editorial")
                datos = { 
                         'r' : 'Registro '+nom+" Eliminado Correctamente!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'edi' : edi
                        }
                return render(request, 'form_registrar_editorial.html', datos)
                
            except:
                edi = Editorial.objects.all().values().order_by("nombre_editorial")
                datos = { 
                         'r2' : 'El ID '+str(id)+" No Existe. Imposible Eliminar!!",
                         'nomUsuario' : request.session["nomUsuario"],
                         'edi' : edi
                        }
                return render(request, 'form_registrar_editorial.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar La Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)



#--------------------------------------------------------------------------------------------------------


def mostrarPerfilAdmin(request,idusu):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario == "ADMIN":
            try:
                usu = Usuario.objects.get(id=idusu)

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'usu' : usu,
                }

                return render(request, 'perfil_admin.html', datos)
            except:
                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'r2':"Perfil de Admin con ID ("+str(id)+") no existe"         
                }

                return render(request, 'menu_admin.html', datos)

            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
        
    else:

        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#--------------------------------------------------------------------------------------------------------


def mostrarPerfilUsuario(request,idusu):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        nomUsuario = request.session.get("nomUsuario")
        if nomUsuario != "ADMIN":
            try:
                usu = Usuario.objects.get(id=idusu)

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'usu' : usu,
                }

                return render(request, 'perfil_usuario.html', datos)
            except:
                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'r2':"Perfil de Admin con ID ("+str(id)+") no existe"         
                }

                return render(request, 'menu_usuario.html', datos)

            
        else:
            datos = { 'r2' : 'No Tiene Permisos Para Acceder Al Menú Del Admin' }
            return render(request, 'index.html', datos)
        
    else:

        datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------



