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
            return template('views/index')
        else:
            return template('views/usuario',logged=request.environ['beaker.session']['user'])
    else:
        return template('views/index')

#Enlazar el css
@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='views/css/')

#Enlazar el javascript
@get('/<filename:re:.*\.js>')
def stylesheets(filename):
    return static_file(filename, root='views/scripts/')



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
    datos_usuario = base.login(request.forms.get('name'), request.forms.get('password'))
    if datos_usuario != None:
        user = Usuario(datos_usuario[0],datos_usuario[1],datos_usuario[2])
    if user != None:
        request.environ['beaker.session']['user'] = user
        request.environ['beaker.session']['logged'] = True 
        return template('views/usuario',logged=user)
    else:         
        return '404 not found'


@post('/logout')
def logout():
    request.environ['beaker.session'].delete()
    return template('views/index')


@post('/publicaciones')
def publicar():
    contenido = request.forms.get('contenido')
    base.addPublicacion(request.environ['beaker.session']['user'],contenido)
    index()




port = 5000
host = "localhost"
bottle.run(app=app,debug=True, reloader=True, host=host, port=port)





