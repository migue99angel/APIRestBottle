import MySQLdb
from Usuario import *
from Publicacion import *
from datetime import datetime

class conexionDB:
    def __init__(self):
        self.db = MySQLdb.connect(host="127.0.0.1",user="miguelAngel",passwd="practicasSIBW",db="Prueba")
        self.db.autocommit = True
        self.cur = self.db.cursor()

    def _getConnection(self):
        return self.db
    
    def _getCursor(self):
        return self.cur

    def close(self):
        self.db.close

    def obtenerUsuarios(self):
        self.cur.execute("SELECT * FROM usuarios")
        users = self.cur.fetchall()
        return users

    def registrarUsuario(self,user,password,email):
        user = self.db.escape_string(user)
        password = self.db.escape_string(password)
        email = self.db.escape_string(email)
        query = "INSERT INTO usuarios(user, password, email) VALUES (%s, %s, %s)"
        self.cur.execute(query,((user, password, email)))
        self.db.commit()

    def login(self,name, password):
        self.cur.execute("SELECT * FROM usuarios where user=%s AND password=%s",(name,password))
        datos =  self.cur.fetchone()
        user = Usuario(datos[0],datos[1],datos[2])
        self.cargarPublicaciones(user)
        return user

    def addPublicacion(self,user,contenido):
        now = datetime.now()
        email = user.email
        name = user.name
        fecha = now.strftime("%Y-%m-%d")
        self.cur.execute("INSERT INTO publicaciones(email, nombre, fecha, contenido) VALUES (%s, %s, %s, %s)",((email, name, fecha, contenido)))
        self.db.commit()
        return self.cargarPublicaciones(user)

    def cargarPublicaciones(self,user):
        email = user.email
        self.cur.execute("SELECT * FROM publicaciones where email=%s",[email])
        publicaciones =  self.cur.fetchall()
        user.cargarPublicaciones(publicaciones)
        return user