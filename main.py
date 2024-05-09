#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# main.py: 
# Programa python para gestionar una pequeña base de datos
#
# Autor: Pablo Vilán Mancuello (pablo.viland@udc.es)
# Autor: 
#

import psycopg2;
import psycopg2.errorcodes
import psycopg2.extras;

# Parámetros de conexión
dbname = 'bda'
user = ''
password = ''
host = ''  

## ------------------------------------------------------------
def connect_db():

    try:
        #conn = psycopg2.connect(dbname=dbname, user=user, password=password)
        conn = psycopg2.connect(dbname=dbname)

        conn.autocommit = False
        
        return conn
    
    except psycopg2.OperationalError as e:
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            print("Cancelando transacción..")
            return None


## ------------------------------------------------------------
def disconnect_db(conn):
    
    try:
        if conn is not None:
            conn.close()
        else:
            print("No hay una conexión que cerrar")

    except psycopg2.OperationarError as e:
        print("Error al desconectar de la base de datos")
        return None
    
##-------------------------------------------------------------
def add_product(conn):
    """Pide por teclado numero referencia, nombre, colección, si es personalizable,
    y su referencia a categoria
    """
    n_reference = input("Número de Referencia: ")
    name = input("Nombre: ")
    colection = input("Colección: ")
    if colection == "": colection = None
    sisPersonalizable = input("Es personalizable y/[n]") ## por defecto no es personalizable
    isPersonalizable = False
    if sisPersonalizable == "y": isPersonalizable = True
    scategory_id = input("Id categoria: ")
    category_id = int(scategory_id)

    sql="""
            INSERT INTO Producto(nombre,numero_referencia,coleccion,es_personalizable,
            id_categoria) values(%(n)s, %(r)s, %(c)s, %(p)s, %(i)s) returning id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':name, 'r':n_reference, 'c': colection, 'p':isPersonalizable,
                              'i':category_id})  
            conn.commit()
            id = cur.fetchone()[0]
            print("Producto Añadido con id: {id}.")
        except psycopg2.Error as e:
            print(f"Error al añadir el producto: {e}")
            conn.rollback()
##-------------------------------------------------------------
def add_color(conn):
    """
    Añade un nuevo color a la base de datos y muestra el ID del color añadido.
    """
    s_product_id = input("Id del Producto que se quiere añadir un nuevo color: ")

    if s_product_id is "":
        print("Debes introducit un id de producto")
        return
    product_id = int(s_product_id)
    
    color_name = input("Color del Producto: ")
    if color_name is "":
        print("Debes introducir un color de producto")
        return
    
    sprice = input("Precio del producto")
    price = float(sprice)
    
    composition = input("Composición: ")
    if composition is "":
        print("Debes introducir una composicion")
        return
    
    cursor = conn.cursor()

    sql="""
            "INSERT INTO Color(nombre, precio, composicion, id_producto) 
            VALUES (%(n)s, %(p)s, %(c)s, %(i)s) RETURNING id"
        """
    
    try:
        # Inserta el color en la tabla y retorna el ID autogenerado
        cursor.execute(sql, {'n': color_name, 'p': price, 'c': composition, 'i': product_id})
        # Recupera el ID del color recién insertado
        color_id = cursor.fetchone()[0]
        conn.commit()  # Confirma la transacción
        print(f"Color añadido con éxito. ID: {color_id}")
    except psycopg2.Error as e:
        # Maneja cualquier error que ocurra durante la inserción
        conn.rollback()
        print(f"Error al añadir color: {e}")


##-------------------------------------------------------------
def add_category(conn):
    """
    Pide por teclado nombre de categoria y devuelve el id autogenerado
    si la inserción en BD se realiza correctamente
    """

    category_name = input("Nombre categoria: ")
    if category_name ==  "":
        print("Debes introducir un nombre de categoria")
        return

    sql="""
            INSERT INTO Categoria(nombre) values(%(n)s) returning id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':category_name}) 
            conn.commit() 
            id = cur.fetchone()[0]
            print(f"Categoria Añadido con id: {id}.")
        except psycopg2.Error as e:
            print(f"Error al añadir la categoria: {e}")
            conn.rollback()

    
## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opciones, solicita la opción y ejecuta la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
      -- MENÚ --
 1 - Añadir Producto         2 - Añadir Color        3 - Eliminar Producto
 4 - Eliminar Color          5 - Añadir Categoria    6 - Eliminar Categoria
 7 - Oferta Producto         8 - Oferta Categoria    9 - Categorias de Oferta
10 - Productos de Oferta    11 - Ofertas            12 - Terminar oferta
13 - Comparar precio antes y despues de Oferta
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            add_product(conn)
        elif tecla == '2':
            add_color(conn)
        elif tecla == '5':
            add_category(conn)



def main():
    """
    Función principal. Conecta a la bd y ejecuta el menú.
    Al salir del menu, desconecta la BD y finaliza el programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)


if __name__ == '__main__':
    main()



