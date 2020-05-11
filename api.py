from bottle import *
import bottle_session
import bottle
import beaker.middleware

session_opts = {
    'session.type': 'file',
    'session.data_dir': './.session/',
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)



users = [{'name' : 'illomigue', 'type' : 'superuser','password' : '1234' },
          {'name' : 'd3vcho', 'type' : 'superuser','password' : '1234'},
          {'name' : 'Direkk', 'type' : 'standard','password' : '1234'},
          {'name' : 'corderop', 'type' : 'standard','password' : '1234'},
          {'name' : 'currobeltran', 'type' : 'standard','password' : '1234'}]


#Antes de atender cualquier peticion, almacenamos la sesion de beaker en request.session, es el equivalente a session_start() que utilizamos en php
@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@get('/')
def index():
    if 'logued' in request.environ['beaker.session']:
        if request.environ['beaker.session']['logued'] == False :
            return template('views/index')
        else:
            for user in users:
                if user['name'] == request.session['username']:
                    logued = user
            return template('views/usuario',logued=logued)
    else:
        return template('views/index')

#Enlazar el css
@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='views/css/')



@get('/users')
def getAll():
    return {'users' : users}


@get('/users/<name>')
def getUser(name):
    search = {'' : '', '' : ''}
    for user in users:
        if(user['name'] == name):
            search = user
        
    return search


#Esta funcion recibe un objeto en formato JSON
@post('/users')
def addUser():
    new_user = {'name' : request.forms.get('name'), 'type' : request.forms.get('type')}
    users.append(new_user)
    return {'users' : users}

@post('/login')
def login():
    log_user = {'name' : request.forms.get('name'), 'password' : request.forms.get('password')}
    for user in users:
        if user['name'] == log_user['name'] and user['password'] == log_user['password'] :
            logued = user
            request.environ['beaker.session']['username'] = log_user['name']
            request.environ['beaker.session']['logued'] = True 
            return template('views/usuario',logued=logued)
        
    return '404 not found'


@post('/logout')
def logout():
    request.environ['beaker.session'].delete()
    return template('views/index')



@delete('/users/<name>')
def deleteUser(name):
    search = {'' : '', '' : ''}
    for user in users:
        if(user['name'] == name):
            search = user

    if(search.get('name') == ''):        
        users.remove(search)

    return {'users' : users}




bottle.run(app=app,debug=True, reloader=True)





