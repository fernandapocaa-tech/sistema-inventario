# Sistema de Inventario - Tarea 1
# Implementa los 5 modulos descritos en el documento (Descomposicion)
# Ahora guarda el inventario en un archivo (inventario.json) para que no se pierda al cerrar

import json
import os

ARCHIVO = "inventario.json"
IVA = 0.13  # 13% de IVA
inventario = []  # lista de diccionarios, cada uno representa un producto


def cargar_inventario():
    """Se ejecuta al iniciar el programa: si existe el archivo, carga los productos guardados."""
    global inventario
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            inventario = json.load(f)


def guardar_inventario():
    """Se ejecuta despues de cada cambio: guarda el inventario actual en el archivo."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, ensure_ascii=False, indent=2)


def buscar_producto(codigo):
    """Patron reutilizado: buscar un producto por codigo en la lista."""
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None


def registrar_producto():
    # --- ENTRADA ---
    codigo = input("Codigo del producto: ")
    if buscar_producto(codigo) is not None:
        print("Error: ya existe un producto con ese codigo.\n")
        return

    nombre = input("Nombre del producto: ")
    cantidad = int(input("Cantidad inicial: "))
    precio = float(input("Precio: "))

    # --- PROCESO ---
    nuevo = {"codigo": codigo, "nombre": nombre, "cantidad": cantidad, "precio": precio}
    inventario.append(nuevo)
    guardar_inventario()

    # --- SALIDA ---
    print(f"Producto '{nombre}' registrado con exito.\n")


def actualizar_existencias():
    # --- ENTRADA ---
    codigo = input("Codigo del producto a modificar: ")
    producto = buscar_producto(codigo)
    if producto is None:
        print("Error: producto no encontrado.\n")
        return

    tipo = input("Tipo de movimiento (entrada/venta): ").lower()
    cantidad = int(input("Cantidad: "))

    # --- PROCESO ---
    if tipo == "entrada":
        producto["cantidad"] += cantidad
    elif tipo == "venta":
        if producto["cantidad"] >= cantidad:
            producto["cantidad"] -= cantidad
        else:
            print("Error: stock insuficiente.\n")
            return
    else:
        print("Error: tipo de movimiento invalido.\n")
        return

    guardar_inventario()

    # --- SALIDA ---
    print(f"Stock actualizado. Nueva cantidad de '{producto['nombre']}': {producto['cantidad']}\n")


def consultar_stock():
    codigo = input("Codigo del producto a consultar: ")
    producto = buscar_producto(codigo)
    if producto is None:
        print("Error: producto no encontrado.\n")
        return
    precio_sin_iva = producto["precio"]
    precio_con_iva = precio_sin_iva * (1 + IVA)
    print(f"{producto['nombre']} | Stock: {producto['cantidad']} | "
          f"Precio sin IVA: ${precio_sin_iva:.2f} | Precio con IVA (13%): ${precio_con_iva:.2f}\n")


def generar_reporte():
    if not inventario:
        print("El inventario esta vacio.\n")
        return

    valor_total_sin_iva = 0
    print("--- Reporte de inventario ---")
    for producto in inventario:
        subtotal = producto["cantidad"] * producto["precio"]
        valor_total_sin_iva += subtotal
        alerta = " (POCO STOCK)" if producto["cantidad"] < 5 else ""
        print(f"{producto['codigo']} - {producto['nombre']}: {producto['cantidad']} unidades{alerta}")

    valor_total_con_iva = valor_total_sin_iva * (1 + IVA)
    print(f"Valor total del inventario (sin IVA): ${valor_total_sin_iva:.2f}")
    print(f"Valor total del inventario (con IVA 13%): ${valor_total_con_iva:.2f}\n")


def eliminar_producto():
    codigo = input("Codigo del producto a eliminar: ")
    producto = buscar_producto(codigo)
    if producto is None:
        print("Error: producto no encontrado.\n")
        return
    inventario.remove(producto)
    guardar_inventario()
    print("Producto eliminado con exito.\n")


def menu():
    cargar_inventario()  # al arrancar, recupera lo que ya estaba guardado
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
            registrar_producto()
        elif opcion == "2":
            actualizar_existencias()
        elif opcion == "3":
            consultar_stock()
        elif opcion == "4":
            generar_reporte()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida, intenta de nuevo.\n")


if __name__ == "__main__":
    menu()