# Sistema de Inventario – Fase 1

## Qué hace el programa

Es un sistema de inventario por consola que permite:

- Registrar productos nuevos (código, nombre, cantidad y precio).
- Actualizar existencias mediante movimientos de **entrada** o **venta**.
- Consultar el stock y el precio de un producto (con y sin IVA del 13%).
- Generar un reporte general del inventario, marcando los productos con **poco stock** (menos de 5 unidades) y calculando el valor total (con y sin IVA).
- Eliminar productos del inventario.

Todos los cambios se guardan automáticamente en `inventario.json`, por lo que el inventario persiste entre ejecuciones del programa.

## Cómo ejecutarlo

Requiere Python 3 (no necesita librerías externas).

```bash
python main.py
```

Esto carga el inventario guardado (si existe) y muestra un menú interactivo con las 6 opciones del sistema. Para salir, elige la opción `6`.

Para correr las pruebas automáticas (sin necesidad de escribir datos manualmente):

```bash
python tests.py
```

## Estructura del proyecto

```
inventario.py     → funciones propias del sistema (lógica, sin input/print)
main.py            → programa principal: menú, entrada/salida y persistencia
tests.py           → pruebas con distintos casos de datos
inventario.json    → archivo donde se guarda el inventario (se crea automáticamente)
```

Se separó la **lógica** (`inventario.py`) de la **interacción con el usuario** (`main.py`): las funciones en `inventario.py` no usan `input()` ni `print()`, solo reciben datos y retornan resultados. Esto permite reutilizarlas y probarlas (`tests.py`) sin depender del menú.

## Funciones (parámetros y retorno)

Todas las funciones están en `inventario.py` y se conectan entre sí: por ejemplo, `registrar_producto()` usa `buscar_producto()` y `validar_datos_producto()`; `generar_reporte()` usa `validar_stock_bajo()` y `calcular_precio_con_iva()`; `consultar_stock()` usa `buscar_producto()` y `calcular_precio_con_iva()`. Ninguna función queda aislada: todas son invocadas desde `main.py` (o desde otra función).

| Función | Parámetros | Retorna |
|---|---|---|
| `buscar_producto(inventario, codigo)` | lista de productos, código a buscar | `dict` del producto, o `None` si no existe |
| `validar_datos_producto(cantidad, precio)` | cantidad, precio | `(bool, str)` — válido o no, y mensaje de error |
| `calcular_precio_con_iva(precio, iva=0.13)` | precio sin IVA, tasa de IVA | `float` — precio con IVA incluido |
| `validar_stock_bajo(cantidad, umbral=5)` | cantidad actual, umbral mínimo | `bool` — `True` si el stock es bajo |
| `registrar_producto(inventario, codigo, nombre, cantidad, precio)` | lista de productos y datos del nuevo producto | `(bool, str)` — éxito y mensaje |
| `actualizar_existencias(inventario, codigo, tipo, cantidad)` | lista, código, tipo de movimiento (`entrada`/`venta`), cantidad | `(bool, str)` — éxito y mensaje |
| `consultar_stock(inventario, codigo)` | lista de productos, código a consultar | `dict` con nombre, cantidad, precio sin/con IVA, o `None` si no existe |
| `generar_reporte(inventario, umbral_stock_bajo=5)` | lista de productos, umbral de stock bajo | `dict` con detalle por producto y totales (con/sin IVA) |
| `eliminar_producto(inventario, codigo)` | lista de productos, código a eliminar | `(bool, str)` — éxito y mensaje |
| `cargar_inventario(archivo)` | ruta del archivo JSON | `list` — inventario cargado (vacío si no existe el archivo) |
| `guardar_inventario(inventario, archivo)` | lista de productos, ruta del archivo | `bool` — `True` cuando termina de guardar |

## Decisiones y repeticiones utilizadas

- **Condicionales (`if`/`elif`/`else`):** validación de datos, tipo de movimiento (entrada/venta), existencia de productos, opciones del menú.
- **Repetición (`for`):** recorrido del inventario en `buscar_producto()` y `generar_reporte()`.
- **Repetición (`while`):** bucle principal del menú en `main.py`, que se repite hasta que el usuario elige salir.

## Pruebas realizadas

En `tests.py` se ejecutan 6 casos distintos sobre las funciones (cumpliendo el mínimo de 3 pedido):

1. Registrar dos productos válidos.
2. Registrar un producto con código repetido (debe fallar).
3. Actualizar existencias: una entrada válida y una venta con stock insuficiente.
4. Consultar stock de un producto existente y de uno inexistente.
5. Generar el reporte del inventario completo.
6. Eliminar un producto existente y uno inexistente.

También se probó el flujo completo a través de `main.py` (registrar, consultar, generar reporte y salir), confirmando que los datos quedan guardados correctamente en `inventario.json`.

## Equipo – parte de código desarrollada por cada integrante

> Completar con los nombres reales y la parte que hizo cada quien (debe reflejarse también en los commits de GitHub).

- **Nombre 1** – implementó `buscar_producto()`, `validar_datos_producto()` y `calcular_precio_con_iva()` en `inventario.py`.
- **Nombre 2** – implementó `registrar_producto()` y `actualizar_existencias()` en `inventario.py`.
- **Nombre 3** – implementó `consultar_stock()`, `generar_reporte()` y `validar_stock_bajo()` en `inventario.py`.
- **Nombre 4** – implementó `eliminar_producto()`, `cargar_inventario()`, `guardar_inventario()` y el programa principal `main.py`.
- **Nombre 5** (si aplica) – implementó `tests.py` y verificó los casos de prueba.
