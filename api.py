from bottle import run,route, template, get, post, request, delete

users = [{'name' : 'illomigue', 'type' : 'superuser'},
          {'name' : 'd3vcho', 'type' : 'superuser'},
          {'name' : 'Direkk', 'type' : 'standard'},
          {'name' : 'corderop', 'type' : 'standard'},
          {'name' : 'currobeltran', 'type' : 'standard'}]



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
    new_user = {'name' : request.json.get('name'), 'type' : request.json.get('type')}
    users.append(new_user)
    return {'users' : users}



@delete('/users/<name>')
def deleteUser(name):
    search = {'' : '', '' : ''}
    for user in users:
        if(user['name'] == name):
            search = user

    if(search.get('name') == ''):        
        users.remove(search)

    return {'users' : users}


    

if __name__ == '__main__':
    run(debug=True, reloader=True)





