from Publicacion import *
class Usuario:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.amigos = []
        self.seguidores = []

        

    def cargarPublicaciones(self,publicaciones):
        self.publicaciones = []
        for p in publicaciones:
            self.publicaciones.append(Publicacion(p[2],p[4],p[3],p[1]))

    def addAmigo(self,amigo):
        self.amigos.append(amigo)

    def addSeguidor(self,seguidor):
        self.seguidores.append(seguidor)

    def limpiarAmigos(self):
        self.amigos = []

    def limpiarSeguidores(self):
        self.seguidores = []
