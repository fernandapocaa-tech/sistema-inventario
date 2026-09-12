# inventario.py
# Funciones propias del sistema de inventario.
# Cada funcion recibe parametros de entrada y retorna un valor.
# Ninguna funcion queda aislada: se conectan entre si y se usan desde main.py.

import json
import os

IVA = 0.13  # 13% de IVA


def buscar_producto(inventario, codigo):
    """
    Busca un producto dentro del inventario por su codigo.

    Parametros:
        inventario (list): lista de diccionarios, cada uno un producto.
        codigo (str): codigo del producto a buscar.

    Retorna:
        dict con el producto si se encuentra, o None si no existe.
    """
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None


def validar_datos_producto(cantidad, precio):
    """
    Valida que la cantidad y el precio de un producto sean correctos.

    Parametros:
        cantidad (int): cantidad de unidades.
        precio (float): precio unitario.

    Retorna:
        tuple (bool, str): (True, "") si los datos son validos,
        o (False, mensaje_de_error) si no lo son.
    """
    if cantidad < 0 or precio < 0:
        return False, "La cantidad y el precio no pueden ser negativos."
    return True, ""


def calcular_precio_con_iva(precio, iva=IVA):
    """
    Calcula el precio final de un producto aplicando el IVA.

    Parametros:
        precio (float): precio sin IVA.
        iva (float): tasa de IVA a aplicar (por defecto, la constante IVA = 0.13).

    Retorna:
        float: precio final con IVA incluido.
    """
    return precio * (1 + iva)


def validar_stock_bajo(cantidad, umbral=5):
    """
    Determina si la cantidad de un producto representa stock bajo.

    Parametros:
        cantidad (int): cantidad actual en stock.
        umbral (int): cantidad minima aceptable (por defecto 5).

    Retorna:
        bool: True si el stock esta por debajo del umbral, False si no.
    """
    return cantidad < umbral


def registrar_producto(inventario, codigo, nombre, cantidad, precio):
    """
    Registra un nuevo producto en el inventario, usando validar_datos_producto()
    y buscar_producto() para verificar que los datos sean correctos.

    Parametros:
        inventario (list): lista de productos donde se registrara el nuevo producto.
        codigo (str): codigo unico del producto.
        nombre (str): nombre del producto.
        cantidad (int): cantidad inicial en stock.
        precio (float): precio unitario sin IVA.

    Retorna:
        tuple (bool, str): (True, mensaje_de_exito) si se registro correctamente,
        o (False, mensaje_de_error) si no se pudo registrar.
    """
    if buscar_producto(inventario, codigo) is not None:
        return False, f"Error: ya existe un producto con el codigo '{codigo}'."

    valido, mensaje_error = validar_datos_producto(cantidad, precio)
    if not valido:
        return False, f"Error: {mensaje_error}"

    inventario.append({
        "codigo": codigo,
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio,
    })
    return True, f"Producto '{nombre}' registrado con exito."


def actualizar_existencias(inventario, codigo, tipo, cantidad):
    """
    Actualiza el stock de un producto existente (entrada o venta),
    usando buscar_producto() para localizarlo.

    Parametros:
        inventario (list): lista de productos.
        codigo (str): codigo del producto a modificar.
        tipo (str): tipo de movimiento, "entrada" o "venta".
        cantidad (int): cantidad a sumar o restar del stock.

    Retorna:
        tuple (bool, str): (True, mensaje_de_exito) si se actualizo el stock,
        o (False, mensaje_de_error) si no se pudo actualizar.
    """
    producto = buscar_producto(inventario, codigo)
    if producto is None:
        return False, "Error: producto no encontrado."

    tipo = tipo.lower()
    if tipo == "entrada":
        producto["cantidad"] += cantidad
    elif tipo == "venta":
        if producto["cantidad"] < cantidad:
            return False, "Error: stock insuficiente."
        producto["cantidad"] -= cantidad
    else:
        return False, "Error: tipo de movimiento invalido."

    return True, f"Stock actualizado. Nueva cantidad de '{producto['nombre']}': {producto['cantidad']}."


def consultar_stock(inventario, codigo):
    """
    Consulta la informacion de stock y precios de un producto,
    usando buscar_producto() y calcular_precio_con_iva().

    Parametros:
        inventario (list): lista de productos.
        codigo (str): codigo del producto a consultar.

    Retorna:
        dict con nombre, cantidad, precio_sin_iva y precio_con_iva,
        o None si el producto no existe.
    """
    producto = buscar_producto(inventario, codigo)
    if producto is None:
        return None

    return {
        "nombre": producto["nombre"],
        "cantidad": producto["cantidad"],
        "precio_sin_iva": producto["precio"],
        "precio_con_iva": calcular_precio_con_iva(producto["precio"]),
    }


def generar_reporte(inventario, umbral_stock_bajo=5):
    """
    Genera un reporte general del inventario, usando validar_stock_bajo()
    y calcular_precio_con_iva().

    Parametros:
        inventario (list): lista de productos.
        umbral_stock_bajo (int): cantidad minima antes de marcar "poco stock".

    Retorna:
        dict con:
            "detalle": lista de productos con su info y bandera de stock bajo,
            "total_sin_iva": valor total del inventario sin IVA,
            "total_con_iva": valor total del inventario con IVA.
    """
    detalle = []
    total_sin_iva = 0

    for producto in inventario:
        subtotal = producto["cantidad"] * producto["precio"]
        total_sin_iva += subtotal
        detalle.append({
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "cantidad": producto["cantidad"],
            "stock_bajo": validar_stock_bajo(producto["cantidad"], umbral_stock_bajo),
        })

    total_con_iva = calcular_precio_con_iva(total_sin_iva)

    return {
        "detalle": detalle,
        "total_sin_iva": total_sin_iva,
        "total_con_iva": total_con_iva,
    }


def eliminar_producto(inventario, codigo):
    """
    Elimina un producto del inventario, usando buscar_producto() para localizarlo.

    Parametros:
        inventario (list): lista de productos.
        codigo (str): codigo del producto a eliminar.

    Retorna:
        tuple (bool, str): (True, mensaje_de_exito) si se elimino,
        o (False, mensaje_de_error) si no se encontro el producto.
    """
    producto = buscar_producto(inventario, codigo)
    if producto is None:
        return False, "Error: producto no encontrado."

    inventario.remove(producto)
    return True, "Producto eliminado con exito."


def cargar_inventario(archivo):
    """
    Carga el inventario guardado en un archivo JSON.

    Parametros:
        archivo (str): ruta del archivo JSON a leer.

    Retorna:
        list: lista de productos cargada desde el archivo,
        o una lista vacia si el archivo no existe.
    """
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_inventario(inventario, archivo):
    """
    Guarda el inventario actual en un archivo JSON.

    Parametros:
        inventario (list): lista de productos a guardar.
        archivo (str): ruta del archivo JSON donde se guardara.

    Retorna:
        bool: True cuando el guardado se completa correctamente.
    """
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(inventario, f, ensure_ascii=False, indent=2)
    return True
