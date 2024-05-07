-- Script de creación de las tablas

-- Crear tabla CATEGORIA
CREATE TABLE Categoria(
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(40) UNIQUE NOT NULL,
);

-- Crear tabla PRODUCTO
CREATE TABLE Producto(
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    numero_referencia VARCHAR(50) UNIQUE NOT NULL,
    coleccion VARCHAR(50),
    es_personalizable BOOLEAN NOT NULL,
    id_categoria BIGINT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id)
);

-- Crear tabla COLOR
CREATE TABLE Color(
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK(precio > 0),
    composicion VARCHAR(50) NOT NULL,
    id_producto BIGINT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES Producto(id)
);

-- Crear tabla OFERTA
CREATE TABLE Oferta(
    id BIGSERIAL PRIMARY KEY,
    nombre_oferta VARCHAR(50) UNIQUE NOT NULL,
    porcentaje_oferta INT NOT NULL CHECK(porcentaje_oferta > 0 AND porcentaje_oferta < 100),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);

-- Crear tabla OFERTA-ROPA
CREATE TABLE Oferta_Ropa(
    id BIGSERIAL PRIMARY KEY,
    id_oferta BIGINT NOT NULL,
    id_color BIGINT NOT NULL,
    FOREIGN KEY (id_oferta) REFERENCES Oferta(id),
    FOREIGN KEY (id_color) REFERENCES Color(id)
);

-- Crear tabla OFERTA-CATEGORIA
CREATE TABLE Oferta_Categoria(
    id BIGSERIAL PRIMARY KEY,
    id_oferta BIGINT NOT NULL,
    id_categoria BIGINT NOT NULL,
    FOREIGN KEY (id_oferta) REFERENCES Oferta(id),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id)
);