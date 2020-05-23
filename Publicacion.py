from Comentario import *
class Publicacion:
    def __init__(self,nombre,contenido,fecha,idPublicacion):
        self.nombre = nombre
        self.contenido = contenido
        self.fecha = fecha
        self.id = idPublicacion
        self.comentarios = []

    def addComentario(self,comen):
        self.comentarios.append(comen)

    def cargarComentarios(self,comentarios):
        for c in comentarios:
            aux = Comentario(c[0],c[1],c[2],c[3],c[4],c[5])
            self.addComentario(aux)