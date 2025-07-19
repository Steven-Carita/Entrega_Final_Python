import sqlite3
from colorama import Fore, Style, init

# Inicializamos colorama
init(autoreset=True)

# Funcion para crear la base de datos y la tabla de productos si no existen
def crear_base_datos():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit() # Guardamos los cambios
    conn.close()  # Cerramos la conexion con la base de datos

# Funcion para agregar un nuevo producto al inventario
def agregar_producto():
    print(Fore.CYAN + "\n-- Agregar nuevo producto --")
    
    # Solicitamos al usuario los datos del producto
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripcion: ").strip()
    cantidad = input("Cantidad: ").strip()
    precio = input("Precio: ").strip()
    categoria = input("Categoria: ").strip()

    # Validamos que cantidad y precio sean valores numericos, y que nombre no este vacio
    if not (nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit()):
        print(Fore.RED + "Error: nombre, cantidad o precio invalidos.")
        return

    # Insertamos los datos en la base de datos
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, int(cantidad), float(precio), categoria))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto agregado correctamente.")

# Funcion para mostrar todos los productos registrados
def mostrar_productos():
    print(Fore.CYAN + "\n-- Lista de productos --")
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

     # Si no hay productos, informa al usuario
    if not productos:
        print(Fore.YELLOW + "No hay productos registrados.")
    else:
        # Mostramos todos los productos
        for prod in productos:
            print(Fore.WHITE + f"ID: {prod[0]} | Nombre: {prod[1]} | Cantidad: {prod[3]} | Precio: ${prod[4]} | Categoria: {prod[5]}")

# Funcion para buscar un producto por su ID
def buscar_producto_por_id():
    print(Fore.CYAN + "\n-- Buscar producto por ID --")
    id_str = input("Ingrese el ID del producto: ").strip()
    if not id_str.isdigit():
        print(Fore.RED + "ID invalido.")
        return

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (int(id_str),))
    producto = cursor.fetchone()
    conn.close()

    # Muestra el producto si fue encontrado
    if producto:
        print(Fore.WHITE + f"ID: {producto[0]} | Nombre: {producto[1]} | Descripcion: {producto[2]} | Cantidad: {producto[3]} | Precio: ${producto[4]} | Categoria: {producto[5]}")
    else:
        print(Fore.YELLOW + "Producto no encontrado.")

# Funcion para buscar productos por nombre o categoria
def buscar_por_nombre_o_categoria():
    print(Fore.CYAN + "\n-- Buscar por nombre o categoria --")
    palabra = input("Ingrese nombre o categoria a buscar: ").strip().lower()
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM productos
        WHERE LOWER(nombre) LIKE ? OR LOWER(categoria) LIKE ?
    ''', (f"%{palabra}%", f"%{palabra}%"))
    resultados = cursor.fetchall()
    conn.close()

     # Muestra los resultados encontrados
    if resultados:
        for prod in resultados:
            print(Fore.WHITE + f"ID: {prod[0]} | Nombre: {prod[1]} | Cantidad: {prod[3]} | Precio: ${prod[4]} | Categoria: {prod[5]}")
    else:
        print(Fore.YELLOW + "No se encontraron productos.")

# Funcion para actualizar los datos de un producto especifico
def actualizar_producto():
    print(Fore.CYAN + "\n-- Actualizar producto --")
    id_str = input("ID del producto a actualizar: ").strip()
    if not id_str.isdigit():
        print(Fore.RED + "ID invalido.")
        return

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (int(id_str),))
    producto = cursor.fetchone()
    if not producto:
        print(Fore.YELLOW + "Producto no encontrado.")
        return

    print(Fore.YELLOW + "Dejar en blanco para no modificar un campo.")
    
    # Permite al usuario dejar campos en blanco para conservar los valores anteriores
    nombre = input(f"Nuevo nombre ({producto[1]}): ") or producto[1]
    descripcion = input(f"Nueva descripcion ({producto[2]}): ") or producto[2]
    cantidad = input(f"Nueva cantidad ({producto[3]}): ") or producto[3]
    precio = input(f"Nuevo precio ({producto[4]}): ") or producto[4]
    categoria = input(f"Nueva categoria ({producto[5]}): ") or producto[5]

    try:
        cursor.execute('''
            UPDATE productos
            SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
            WHERE id=?
        ''', (nombre, descripcion, int(cantidad), float(precio), categoria, int(id_str)))
        conn.commit()
        print(Fore.GREEN + "Producto actualizado correctamente.")
    except Exception as e:
        print(Fore.RED + f"Error al actualizar: {e}")
    finally:
        conn.close()

# Funcion para eliminar un producto por su ID
def eliminar_producto():
    print(Fore.CYAN + "\n-- Eliminar producto --")
    id_str = input("ID del producto a eliminar: ").strip()
    if not id_str.isdigit():
        print(Fore.RED + "ID invalido.")
        return

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (int(id_str),))
    conn.commit()
    if cursor.rowcount:
        print(Fore.GREEN + "Producto eliminado.")
    else:
        print(Fore.YELLOW + "No se encontro el producto.")
    conn.close()

# Funcion para mostrar un reporte de productos con bajo stock
def reporte_bajo_stock():
    print(Fore.CYAN + "\n-- Reporte de bajo stock --")
    limite = input("Ingrese el limite de stock: ").strip()
    if not limite.isdigit():
        print(Fore.RED + "Debe ingresar un numero.")
        return

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (int(limite),))
    productos = cursor.fetchall()
    conn.close()

    # Muestra los productos cuyo stock esta por debajo o igual al limite ingresado
    if productos:
        print(Fore.MAGENTA + f"\nProductos con stock menor o igual a {limite}:")
        for p in productos:
            print(Fore.WHITE + f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]} | Precio: ${p[4]} | Categoria: {p[5]}")
    else:
        print(Fore.YELLOW + "No hay productos con stock bajo.")

# Funcion principal que muestra el menu del sistema
def menu():
    crear_base_datos() # Nos aseguramos de que la base de datos y tabla existan antes de comenzar
    while True:
        print(Fore.CYAN + "\n--- MENU PRINCIPAL - GESTOR DE INVENTARIO - STEVEN TECHNOLOGY ---")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto por ID")
        print("4. Buscar por nombre o categoria")
        print("5. Actualizar producto por ID")
        print("6. Eliminar producto por ID")
        print("7. Reporte de bajo stock")
        print("8. Salir")
        opcion = input(Fore.CYAN + "Seleccione una opcion: ").strip()

         # Ejecuta la funcion correspondiente segun la opcion elegida por el usuario
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto_por_id()
        elif opcion == "4":
            buscar_por_nombre_o_categoria()
        elif opcion == "5":
            actualizar_producto()
        elif opcion == "6":
            eliminar_producto()
        elif opcion == "7":
            reporte_bajo_stock()
        elif opcion == "8":
            print(Fore.MAGENTA + "Gracias por usar el sistema. Hasta luego!")
            break
        else:
            print(Fore.RED + "Opcion invalida.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu()
