from Publicacion import *
class Usuario:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        

    def cargarPublicaciones(self,publicaciones):
        self.publicaciones = []
        for p in publicaciones:
            self.publicaciones.append(Publicacion(p[2],p[4],p[3],p[1]))

