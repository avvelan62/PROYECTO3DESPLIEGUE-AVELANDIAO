from funciones import producto_mas_rentable
from models.producto import Producto
from models.ingrediente import Ingrediente
from decimal import Decimal
from database.db import db

class Heladeria():
    def __init__(self, productos: list[Producto], ingredientes: list[Ingrediente]) -> None:
        self._productos = productos
        self._ingredientes = ingredientes
        self._contador_venta_dia = 0

    # Métodos
    def vender_producto(self, producto_id: int) -> str:
        """Vende un producto de la heladería

        Returns:
            bool: Retorna si logra vender el producto
        """
        for producto in self.productos:
            if producto.id == int(producto_id): 
                existe_ingredientes = True
                
                for ingrediente in [producto.ingrediente_1, producto.ingrediente_2, producto.ingrediente_3]:  
                    if ingrediente.tipo == "Complemento" and ingrediente.inventario < 1:
                        raise ValueError(ingrediente.nombre)
                    elif ingrediente.tipo == "Base" and ingrediente.inventario < 0.2:
                        raise ValueError(ingrediente.nombre) 
                
                if existe_ingredientes:
                    # Si todos los ingredientes tienen inventario suficiente, se resta inventario y actualiza ventas
                    for ingrediente in [producto.ingrediente_1, producto.ingrediente_2, producto.ingrediente_3]:
                        if ingrediente.tipo == "Complemento":
                            ingrediente.inventario -= Decimal(1)
                        elif ingrediente.tipo == "Base":
                            ingrediente.inventario -= Decimal(0.2)

                    db.session.commit()
                    
                    self.contador_venta_dia += producto.precio
                    return "¡Vendido!"
        return "Producto no encontrado"
                
    def producto_mas_rentable(self) -> str:
        """Determina el producto más rentable de la heladería"""                 
        producto_1 = {"nombre": self.productos[0].nombre, "rentabilidad": self.productos[0].precio}
        producto_2 = {"nombre": self.productos[1].nombre, "rentabilidad": self.productos[1].precio}
        producto_3 = {"nombre": self.productos[2].nombre, "rentabilidad": self.productos[2].precio}
        producto_4 = {"nombre": self.productos[3].nombre, "rentabilidad": self.productos[3].precio}
        
        return producto_mas_rentable(producto_1, producto_2, producto_3, producto_4)
    
    # Getter y Setter        
    @property
    def productos(self) -> list[Producto]:
        """ Devuelve el valor del atributo privado 'productos' """
        return self._productos
    
    @productos.setter
    def productos(self, value:list[Producto]) -> None:
        """ 
        Establece un nuevo valor para el atributo privado 'productos'
    
        Valida que el valor enviado corresponda al tipo de dato del atributo
        """ 
        if isinstance(value, list[Producto]):
            self._productos = value
        else:
            raise ValueError('Expected list')

    @property
    def ingredientes(self) -> list[Ingrediente]:
        """ Devuelve el valor del atributo privado 'ingredientes' """
        return self._ingredientes
    
    @ingredientes.setter
    def ingredientes(self, value:list[Ingrediente]) -> None:
        """ 
        Establece un nuevo valor para el atributo privado 'ingredientes'
    
        Valida que el valor enviado corresponda al tipo de dato del atributo
        """ 
        if isinstance(value, list[Ingrediente]):
            self._ingredientes = value
        else:
            raise ValueError('Expected list[Ingrediente]')
    
    @property
    def contador_venta_dia(self) -> int:
        """ Devuelve el valor del atributo privado 'contador_venta_dia' """
        return self._contador_venta_dia
    
    @contador_venta_dia.setter
    def contador_venta_dia(self, value:int) -> None:
        """ 
        Establece un nuevo valor para el atributo privado 'contador_venta_dia'
    
        Valida que el valor enviado corresponda al tipo de dato del atributo
        """ 
        if isinstance(value, int):
            self._contador_venta_dia = value
        else:
            raise ValueError('Expected int')