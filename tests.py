# tests.py
# Pruebas del sistema con distintos casos de datos.
# Usa las funciones de inventario.py directamente (sin pasar por el menu),
# para verificar que cada una retorna el resultado esperado.

from inventario import (
    registrar_producto,
    actualizar_existencias,
    consultar_stock,
    generar_reporte,
    eliminar_producto,
)


def ejecutar_pruebas():
    inventario = []

    print("Caso 1: registrar productos validos")
    print(registrar_producto(inventario, "P001", "Cuaderno", 10, 1.50))
    print(registrar_producto(inventario, "P002", "Lapicero", 3, 0.75))

    print("\nCaso 2: registrar un producto con codigo repetido (debe fallar)")
    print(registrar_producto(inventario, "P001", "Cuaderno Grande", 5, 2.00))

    print("\nCaso 3: actualizar existencias (entrada y venta con stock insuficiente)")
    print(actualizar_existencias(inventario, "P001", "entrada", 5))
    print(actualizar_existencias(inventario, "P002", "venta", 10))

    print("\nCaso 4: consultar stock de un producto existente y de uno inexistente")
    print(consultar_stock(inventario, "P001"))
    print(consultar_stock(inventario, "P999"))

    print("\nCaso 5: generar reporte del inventario")
    print(generar_reporte(inventario))

    print("\nCaso 6: eliminar un producto existente y uno inexistente")
    print(eliminar_producto(inventario, "P002"))
    print(eliminar_producto(inventario, "P999"))


if __name__ == "__main__":
    ejecutar_pruebas()
