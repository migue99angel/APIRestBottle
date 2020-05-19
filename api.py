from bottle import *
import bottle_session
import bottle
import beaker.middleware
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",    # tu host, usualmente localhost
                     user="miguelAngel",         # tu usuario
                     passwd="practicasSIBW",  # tu password
                     db="Prueba")        # el nombre de la base de datos

db.autocommit = True

#Debes crear un objeto Cursor. Te permitira ejecutar todos los queries que necesitas
cur = db.cursor()


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
    if 'loged' in request.environ['beaker.session']:
        if request.environ['beaker.session']['loged'] == False :
            return template('views/index')
        else:
            return template('views/usuario',loged=request.environ['beaker.session']['user'])
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
        cur.execute("insert into usuarios(user, password, email) values (%s, %s, %s)",((user, password, email)))
        db.commit()
    else:
        return '<h1>Algo ha salido mal :(</h1>'


@post('/login')
def login():
    log_user = {'name' : request.forms.get('name'), 'password' : request.forms.get('password')}
    cur.execute("SELECT * FROM usuarios where user=%s AND password=%s",(log_user['name'],log_user['password']))
    user =  cur.fetchone()
    if user != None:
        request.environ['beaker.session']['user'] = user
        request.environ['beaker.session']['loged'] = True 
        return template('views/usuario',loged=user)
    else:         
        return '404 not found'


@post('/logout')
def logout():
    request.environ['beaker.session'].delete()
    return template('views/index')




port = 5000
host = "localhost"
bottle.run(app=app,debug=True, reloader=True, host=host, port=port)





