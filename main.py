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
dbname = ''
user = ''
password = ''
host = ''  

## ------------------------------------------------------------
def connect_db():

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)

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
    if n_reference == "": n_reference = None

    name = input("Nombre: ")
    if name == "": name = None

    colection = input("Colección: ")
    if colection == "": colection = None

    sisPersonalizable = input("Es personalizable y/[n]") ## por defecto no es personalizable
    isPersonalizable = False
    if sisPersonalizable == "y": isPersonalizable = True

    scategory_id = input("Id categoria: ")
    category_id = None if scategory_id == "" else int(scategory_id)

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
            print(f"Producto Añadido con id: {id}.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir producto, {e.diag.message_detail}")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"Error al añadir producto, la categoria no existe")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir producto, hay campos que no pueden ser nulos no existe")
            else:
                print(f"Error al añadir el producto: {e}")
            conn.rollback()

##-------------------------------------------------------------
def add_color(conn):
    """
    Añade un nuevo color a la base de datos y muestra el ID del color añadido.
    """
    s_product_id = input("Id del Producto que se quiere añadir un nuevo color: ")
    product_id = None if s_product_id == "" else int(s_product_id)
    
    color_name = input("Color del Producto: ")
    if color_name == "": color_name = None
    
    s_price = input("Precio del producto")
    price = None if s_price == "" else float(s_price)
    
    composition = input("Composición: ")
    if composition == "": composition = None
    
    sql="""
            INSERT INTO Color(nombre, precio, composicion, id_producto) 
            VALUES (%(n)s, %(p)s, %(c)s, %(i)s) RETURNING id
        """
    with conn.cursor() as cur:
        try:
            # Inserta el color en la tabla y retorna el ID autogenerado
            cur.execute(sql, {'n': color_name, 'p': price, 'c': composition, 'i': product_id})
            # Recupera el ID del color recién insertado
            color_id = cur.fetchone()[0]
            conn.commit()  # Confirma la transacción
            print(f"Color añadido con éxito. ID: {color_id}")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir color, {e.diag.message_detail}")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"Error al añadir color, el producto no existe")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir color, el {e.diag.column_name} no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print(f"Error al añadir color, el precio ha de ser > 0")

            else:
                print(f"Error al añadir el color: {e}")
            conn.rollback()

##-------------------------------------------------------------
def delete_product(conn):
    """
    Elimina un color de la base de datos dado un Id introducido por pantalla
    """
    s_product_id = input("Id del Producto: ")
    product_id = None if s_product_id == "" else int(s_product_id)

    sql="""
            DELETE FROM Producto WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'i': product_id})
            conn.commit()
            print(f"Producto con ID: {product_id} eliminado con exito")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar producto: {e}")

##-------------------------------------------------------------
def delete_color(conn):
    """
    Elimina un color de la base de datos dado un Id introducido por pantalla
    """
    s_color_id = input("Id del Producto: ")
    color_id = None if s_color_id == "" else int(s_color_id)

    sql="""
            "DELETE FROM Color WHERE id = %(i)s"
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'i': color_id})
            conn.commit()
            print(f"Color con ID: {color_id} eliminado con exito")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al añadir color: {e}")


##-------------------------------------------------------------
def add_category(conn):
    """
    Pide por teclado nombre de categoria y devuelve el id autogenerado
    si la inserción en BD se realiza correctamente
    """

    category_name = input("Nombre categoria: ")
    if category_name ==  "": category_name = None

    sql="""
            INSERT INTO Categoria(nombre) values(%(n)s) returning id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':category_name}) 
            conn.commit() 
            id = cur.fetchone()[0]
            print(f"Categoria añadida con id: {id}.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir Categoria, el {e.diag.column_name} no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir Categoria, el Nombre ya existe")
            else:
                print(f"Error al añadir la Categoria: {e}, {e.pgcode}")
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
        elif tecla == '3':
            delete_product(conn)
        elif tecla == '4':
            delete_color(conn)
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



