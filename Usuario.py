from Publicacion import *
class Usuario:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.publicaciones = []
        self.amigos = []
        self.seguidores = []

        

    # def cargarPublicaciones(self,publicaciones):
    #     for p in publicaciones:
    #         self.publicaciones.append(Publicacion(p[2],p[4],p[3],p[1]))

    def cargarPublicacion(self, publicacion, comentarios):
        p = Publicacion(publicacion[2],publicacion[4],publicacion[3],publicacion[1])
        p.cargarComentarios(comentarios)
        self.publicaciones.append(p)


    def addAmigo(self,amigo):
        self.amigos.append(amigo)

    def addSeguidor(self,seguidor):
        self.seguidores.append(seguidor)

    def limpiarAmigos(self):
        self.amigos = []

    def limpiarSeguidores(self):
        self.seguidores = []

    
    def limpiarPublicaciones(self):
        self.publicaciones = []

    def sigueA(self,usuario):
        for a in self.amigos:
            if usuario.name == a.name:
                return True

                