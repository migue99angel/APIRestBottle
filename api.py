from bottle import *
import bottle
import beaker.middleware
from conexionDB import *
from Usuario import *

base = conexionDB() #Creo la conexion con la base de datos


session_opts = {
    'session.type': 'file',
    'session.data_dir': './.session/',
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


#Antes de atender cualquier peticion, almacenamos la sesion de beaker en request.session, es el equivalente a session_start() que utilizamos en php
@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@get('/')
def index():
    if 'logged' in request.environ['beaker.session']:
        if request.environ['beaker.session']['logged'] == False :
            return template('views/index',error=0)
        else:
            return template('views/usuario',logged=request.environ['beaker.session']['user'])
    else:
        return template('views/index',error=0)

#Enlazar el css
@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='views/css/')

#Enlazar el javascript
@get('/<filename:re:.*\.js>')
def stylesheets(filename):
    return static_file(filename, root='views/scripts/')

@post('/buscar')
def getUser():
    user = request.forms.get('consulta')
    usuario = base.cargarMuro(user)   
    if usuario != None:
        seguido = request.environ['beaker.session']['user'].sigueA(usuario)
        return template('views/visitar_muro',user=usuario,seguido=seguido)
    else:
        return '<h1>404 Not found</h1>'


@post('/editProfile')
def actualizarPerfil():
    new_name = request.forms.get('username')
    if new_name != None:
        base.actualizarPerfil(request.environ['beaker.session']['user'],new_name)
        request.environ['beaker.session'].delete()
        return redirect('/')
    else:
        return '<h1>Algo ha pasado...</h1>'

# Cambiar nombre desde Android.
@post('/editProfileAPI')
def actualizarPerfilAPI():
    new_name = request.forms.get('username')
    email = request.forms.get('email')

    if new_name != None:
        base.actualizarPerfilAPI(email, new_name)
        request.environ['beaker.session'].delete()
        rv = {
            "respuesta": {
                "cambio": 1
            }
        }
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        rv = {
            "respuesta": {
                "cambio": 0
            }
        }
        response.content_type = 'application/json'
        return dumps(rv)

@post('/users')
def registro():
    if request.forms.get('password') == request.forms.get('confirm_password'):
        user = request.forms.get('name')
        password = request.forms.get('password')
        email = request.forms.get('email')
        base.registrarUsuario(user,password,email)
        
    else:
        return '<h1>Algo ha salido mal :(</h1>'


@post('/login')
def login():
    user = base.login(request.forms.get('name'), request.forms.get('password'))
    if user != None:
        request.environ['beaker.session']['user'] = user
        request.environ['beaker.session']['logged'] = True 
        return redirect('/')
    else:         
        return template('views/index',error=1)

# Login desde Android. Devolvemos JSON con los datos del usuario
@post('/loginAPI')
def loginAPI():
    user = base.login(request.forms.get('name'), request.forms.get('password'))
    if user != None:
        request.environ['beaker.session']['user'] = user
        request.environ['beaker.session']['logged'] = True
        rv = {
            "data": {
                "user": user.name,
                "email": user.email,
                "cantidadAmigos": len(user.amigos),
                "cantidadSeguidores": len(user.seguidores),
                "error": 0
            }
        }
        response.content_type = 'application/json'
        return dumps(rv)
        
    else:         
        rv = {
            "data": {
                "error": 1
            }
        }
        response.content_type = 'application/json'
        return dumps(rv)

@post('/logout')
def logout():
    request.environ['beaker.session'].delete()
    return redirect('/')


@post('/publicaciones')
def publicar():
    contenido = request.forms.get('contenido')
    #Al aniadir la publicacion vuelvo a cargar las publicaciones para mostrar las publicaciones actualizadas
    request.environ['beaker.session']['user'] = base.addPublicacion(request.environ['beaker.session']['user'],contenido)
    return redirect('/')

@post('/addFriend')
def seguir():
    request.environ['beaker.session']['user'] = base.addAmigo(request.environ['beaker.session']['user'],request.forms.get('email'))
    usuario = base.cargarMuro(request.forms.get('name'))
    if usuario != None:
        return template('views/visitar_muro',user=usuario,seguido=True)

@post('/verAmigos')
def verAmigos():
    return template('views/lista_usuarios',lista=request.environ['beaker.session']['user'].amigos)

@post('/verSeguidores')
def verAmigos():
    return template('views/lista_usuarios',lista=request.environ['beaker.session']['user'].seguidores)


@post('/eliminarPublicacion')
def eliminarPublicacion():
    request.environ['beaker.session']['user'] = base.eliminarPublicacion(request.environ['beaker.session']['user'],request.forms.get('id'))
    return redirect('/')

@post('/deleteFriend')
def dejarDeSeguir():
    request.environ['beaker.session']['user'] = base.deleteAmigo(request.environ['beaker.session']['user'],request.forms.get('email'))
    usuario = base.cargarMuro(request.forms.get('name'))
    if usuario != None:
        return template('views/visitar_muro',user=usuario,seguido=False)

port = 5000
host = "localhost"
bottle.run(app=app,debug=True, reloader=True, host=host, port=port)





