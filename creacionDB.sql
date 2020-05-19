--Creo la tabla para los usuarios
CREATE TABLE usuarios(
    user VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE sigue(
    usuario_sigue VARCHAR(50) REFERENCES usuarios(email),
    usuario_seguido VARCHAR(50) REFERENCES usuarios(email),
    PRIMARY KEY(usuario_sigue,usuario_seguido)
);

CREATE TABLE publicaciones(
  idPublicacion INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  fecha DATE,
  contenido TEXT
);

CREATE TABLE publica(
    usuario  VARCHAR(50) REFERENCES usuarios(email),
    idPublicacion INT NOT NULL REFERENCES publicaciones(idPublicacion)
);