# main.py
# Programa principal: menu, entrada/salida y persistencia.
# Usa las funciones de inventario.py (logica pura) para procesar los datos.

from inventario import (
    registrar_producto,
    actualizar_existencias,
    consultar_stock,
    generar_reporte,
    eliminar_producto,
    cargar_inventario,
    guardar_inventario,
)

ARCHIVO = "inventario.json"


def menu_registrar(inventario):
    codigo = input("Codigo del producto: ")
    nombre = input("Nombre del producto: ")
    cantidad = int(input("Cantidad inicial: "))
    precio = float(input("Precio: "))

    exito, mensaje = registrar_producto(inventario, codigo, nombre, cantidad, precio)
    print(mensaje + "\n")
    if exito:
        guardar_inventario(inventario, ARCHIVO)


def menu_actualizar(inventario):
    codigo = input("Codigo del producto a modificar: ")
    tipo = input("Tipo de movimiento (entrada/venta): ")
    cantidad = int(input("Cantidad: "))

    exito, mensaje = actualizar_existencias(inventario, codigo, tipo, cantidad)
    print(mensaje + "\n")
    if exito:
        guardar_inventario(inventario, ARCHIVO)


def menu_consultar(inventario):
    codigo = input("Codigo del producto a consultar: ")
    resultado = consultar_stock(inventario, codigo)

    if resultado is None:
        print("Error: producto no encontrado.\n")
        return

    print(f"{resultado['nombre']} | Stock: {resultado['cantidad']} | "
          f"Precio sin IVA: ${resultado['precio_sin_iva']:.2f} | "
          f"Precio con IVA (13%): ${resultado['precio_con_iva']:.2f}\n")


def menu_reporte(inventario):
    if not inventario:
        print("El inventario esta vacio.\n")
        return

    reporte = generar_reporte(inventario)

    print("--- Reporte de inventario ---")
    for producto in reporte["detalle"]:
        alerta = " (POCO STOCK)" if producto["stock_bajo"] else ""
        print(f"{producto['codigo']} - {producto['nombre']}: {producto['cantidad']} unidades{alerta}")

    print(f"Valor total del inventario (sin IVA): ${reporte['total_sin_iva']:.2f}")
    print(f"Valor total del inventario (con IVA 13%): ${reporte['total_con_iva']:.2f}\n")


def menu_eliminar(inventario):
    codigo = input("Codigo del producto a eliminar: ")
    exito, mensaje = eliminar_producto(inventario, codigo)
    print(mensaje + "\n")
    if exito:
        guardar_inventario(inventario, ARCHIVO)


def menu():
    inventario = cargar_inventario(ARCHIVO)

    while True:
        print("===== SISTEMA DE INVENTARIO =====")
        print("1. Registrar producto")
        print("2. Actualizar existencias")
        print("3. Consultar stock")
        print("4. Generar reporte")
        print("5. Eliminar producto")
        print("6. Salir")
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            menu_registrar(inventario)
        elif opcion == "2":
            menu_actualizar(inventario)
        elif opcion == "3":
            menu_consultar(inventario)
        elif opcion == "4":
            menu_reporte(inventario)
        elif opcion == "5":
            menu_eliminar(inventario)
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida, intenta de nuevo.\n")


if __name__ == "__main__":
    menu()
