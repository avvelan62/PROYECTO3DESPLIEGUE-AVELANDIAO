from decimal import Decimal

def es_sano(calorias: int, es_vegetario: bool) -> bool:
    """Permite determinar si un ingrediente es sano

    Args:
        calorias (int): Total de calorías del ingrediente
        vegetario (bool): Indica si el ingrediente es vegetario

    Returns:
        bool: Resultado si el ingrediente es sano o no
    """
    if calorias < 100 or es_vegetario:
        return True
    return False


def calcular_calorias_producto(lista_calorias_ingrediente: list) -> float:
    """Permite calcular calorías de un producto

    Args:
        lista_calorias (list): Lista de enteros que contiene las calorías de
        cada ingrediente del producto

    Returns:
        float: Resultado de calorías por producto
    """
    cantidad_calorias = round(sum(lista_calorias_ingrediente) * Decimal(0.95), 2)
    return cantidad_calorias


def calcular_costo(ingrediente_uno: dict, ingrediente_dos: dict,ingrediente_tres: dict) -> float:
    """Permite calcular el costo de producir un producto

    Args:
        ingrediente_uno (dict): Diccionario del ingrediente uno
        ingrediente_dos (dict): Diccionario del ingrediente dos
        ingrediente_tres (dict): Diccionario del ingrediente tres

    Returns:
        float: El resultado del costo total para producir el producto
    """
    costo_total = ingrediente_uno["precio"] + ingrediente_dos["precio"] + ingrediente_tres["precio"]
    return costo_total


def calcular_rentabilidad(precio_producto: float, ingrediente_uno: dict, ingrediente_dos: dict,ingrediente_tres: dict) -> float:
    """Permite calcular rentabilidad del producto

    Args:
        precio_producto (float): Precio de venta del producto
        ingrediente_uno (dict): Diccionario del ingrediente uno
        ingrediente_dos (dict): Diccionario del ingrediente dos
        ingrediente_tres (dict): Diccionario del ingrediente tres

    Returns:
        float: El resultado de la rentabilidad del producto
    """
    rentabilidad_producto = precio_producto - (ingrediente_uno["precio"] + ingrediente_dos["precio"] + ingrediente_tres["precio"])
    return rentabilidad_producto


def producto_mas_rentable(producto_uno: dict, producto_dos: dict, producto_tres: dict, producto_cuatro: dict) -> str:
    """Permite identificar el producto mas rentable

    Args:
        producto_uno (dict): Diccionario del producto uno
        producto_dos (dict): Diccionario del producto dos
        producto_tres (dict): Diccionario del producto tres
        producto_cuatro (dict): Diccionario del producto cuatro

    Returns:
        str: El resultado del producto mas rentable
    """
    productos = [producto_uno, producto_dos, producto_tres, producto_cuatro]
    producto_rentable = max(productos, key=lambda producto: producto['rentabilidad'])
    return producto_rentable["nombre"]
