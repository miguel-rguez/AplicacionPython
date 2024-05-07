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
            id_categoria) values(%(n)s, %(r)s, %(c)s, %(p)s, %(i)s)
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':name, 'r':n_reference, 'c': colection, 'p':isPersonalizable,
                              'i':category_id})  
            conn.commit()
            print("Producto Añadido.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"El Producto con referencia{n_reference} ya existe. No se añade")
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



