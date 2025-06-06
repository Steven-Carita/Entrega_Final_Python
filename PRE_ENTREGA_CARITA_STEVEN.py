productos = []

while True:
    print("\n--- Gestor de Productos - STEVEN TECHNOLOGY ---")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto")
    print("4. Eliminar producto")
    print("5. Salir")

    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        # Estructura para Agregar Productos
        while True:
            nombre = input("Ingrese el nombre del componente: ").strip()
            if nombre == "":
                print("El nombre no puede estar vacío. Intente nuevamente.")
                continue

            categoria = input("Ingrese la categoría (ejemplos: PERIFERICO, CPU, GPU, RAM, SSD): ").strip()
            if categoria == "":
                print("La categoria no puede estar vacia. Por Favor, intente nuevamente.")
                continue

            precio_str = input("Ingrese el precio (sin centavos): ").strip()
            if not precio_str.isdigit():
                print("El precio debe ser un numero entero positivo. Por favor, intente nuevamente.")
                continue

            precio = int(precio_str)
            if precio < 0:
                print("El precio no puede ser negativo. Por favor, intente nuevamente.")
                continue

            productos.append([nombre, categoria, precio])
            print("Componente '" + nombre + "' agregado correctamente.")
            break

    elif opcion == "2":
        # Estructura para Mostrar Productos
        if len(productos) == 0:
            print("No hay componentes para mostrar.")
        else:
            print("\nLista de componentes:")
            for i, prod in enumerate(productos, start=1):
                print(str(i) + ". Nombre: " + prod[0] + ", Categoria: " + prod[1] + ", Precio: $" + str(prod[2]))

    elif opcion == "3":
        # Estructura para Buscar algun producto
        if len(productos) == 0:
            print("No hay componentes para buscar.")
        else:
            busqueda = input("Ingrese el nombre o parte del nombre del componente a buscar: ").strip().lower()
            encontrados = []
            for i, prod in enumerate(productos, start=1):
                if busqueda in prod[0].lower():
                    encontrados.append((i, prod))
            if len(encontrados) == 0:
                print("No se encontraron componentes con ese nombre.")
            else:
                print("\nSe encontraron " + str(len(encontrados)) + " componente(s):")
                for i, prod in encontrados:
                    print(str(i) + ". Nombre: " + prod[0] + ", Categoría: " + prod[1] + ", Precio: $" + str(prod[2]))

    elif opcion == "4":
        # Estructura para Eliminar algun producto
        if len(productos) == 0:
            print("No hay componentes para eliminar.")
        else:
            print("\nLista de componentes:")
            for i, prod in enumerate(productos, start=1):
                print(str(i) + ". Nombre: " + prod[0] + ", Categoría: " + prod[1] + ", Precio: $" + str(prod[2]))
            while True:
                opcion_eliminar = input("Ingrese el numero del componente a eliminar: ").strip()
                if not opcion_eliminar.isdigit():
                    print("Debe ingresar un numero valido.")
                    continue
                indice = int(opcion_eliminar)
                if 1 <= indice <= len(productos):
                    eliminado = productos.pop(indice - 1)
                    print("Componente '" + eliminado[0] + "' eliminado correctamente.")
                    break
                else:
                    print("Numero fuera de rango. Intente nuevamente.")

    elif opcion == "5":
        print("Gracias por visitar STEVEN TECHNOLOGY. ")
        break

    else:
        print("Opcion no valida. Intente nuevamente.")
