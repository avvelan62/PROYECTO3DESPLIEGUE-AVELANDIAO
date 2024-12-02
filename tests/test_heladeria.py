import unittest
from app import app
from models.heladeria import Heladeria
from models.producto import Producto
from models.ingrediente import Ingrediente
from decimal import Decimal

class TestHeladeria(unittest.TestCase):

    def setUp(self):
        pass

    def test_ingrediente_es_sano(self):
        """Probar si un ingrediente es sano"""
        ingrediente_1 = Ingrediente(id=1, nombre="Base Vainilla", precio=3500, calorias=100, inventario=22.00, es_vegetariano=True, tipo="Base", sabor="Vainilla")
        ingrediente_2 = Ingrediente(id=7, nombre="Nueces Dulce", precio=1000, calorias=120, inventario=10, es_vegetariano=False, tipo="Complemento", sabor=None)
        self.assertTrue(ingrediente_1.es_sano())
        self.assertFalse(ingrediente_2.es_sano())
        
    def test_abastecer_ingrediente(self):
        """Probar si el abastecimiento de un ingrediente aumenta su inventario"""
        with app.app_context():
            ingrediente_1 = Ingrediente(id=1, nombre="Base Vainilla", precio=3500, calorias=100, inventario=Decimal(20.00), es_vegetariano=True, tipo="Base", sabor="Vainilla")
            ingrediente_1.abastecer()
            ingrediente_2 = Ingrediente(id=7, nombre="Nueces Dulce", precio=1000, calorias=120, inventario=10, es_vegetariano=False, tipo="Complemento", sabor=None)
            ingrediente_2.abastecer()
            self.assertEqual(ingrediente_1.inventario, 25) # El inventario inicio en 20 al abastecer inventario de tipo Base incrementa 5 = 25
            self.assertEqual(ingrediente_2.inventario, 20) # El inventario inicio en 10 al abastecer inventario de tipo Base incrementa 10 = 20

    def test_renovar_inventario_complementos(self):
        """Probar si el método de renovar inventario para complementos actualiza correctamente el inventario"""
        with app.app_context():
            ingrediente_1 = Ingrediente(id=7, nombre="Nueces Dulce", precio=1000, calorias=120, inventario=10, es_vegetariano=False, tipo="Complemento", sabor=None)
            ingrediente_1.renovar_inventario()
            self.assertEqual(ingrediente_1.inventario, 0) # El inventario inicia el 10 al renovar el inventario debe quedar en 0

    def test_calcular_calorias(self):
        """Probar el cálculo de calorías para un producto"""
        with app.app_context():
            producto_1 = Producto.query.filter(Producto.id == 1).first() # Producto de tipo Copa 
            producto_2 = Producto.query.filter(Producto.id == 3).first() # Producto de tipo Malteada
            calorias_producto_1 = producto_1.calcular_calorias()
            calorias_producto_2 = producto_2.calcular_calorias()
            self.assertEqual(calorias_producto_1, 285.00)  # 100 (Base Vainilla) + 50 (Chispas Choco) + 150 (Crema Chantilly) * 0.95 = 285.00
            self.assertEqual(calorias_producto_2, 370.50)  # 120 (Base Chocolate) + 120 (Nueces Dulce) + 150 (Crema Chantilly) * 0.95 = 370.50


    def test_calcular_costo_produccion(self):
        """Probar el cálculo del costo de producción de un producto"""
        with app.app_context():
            producto_1 = Producto.query.filter(Producto.id == 1).first()
            producto_2 = Producto.query.filter(Producto.id == 2).first()
            producto_3 = Producto.query.filter(Producto.id == 3).first()
            producto_4 = Producto.query.filter(Producto.id == 4).first()

            costo_producto_1 = producto_1.calcular_costo()
            costo_producto_2 = producto_2.calcular_costo()
            costo_producto_3 = producto_3.calcular_costo()
            costo_producto_4 = producto_4.calcular_costo()

            self.assertEqual(costo_producto_1, 6000)  # Costo estimado con los ingredientes 6000
            self.assertEqual(costo_producto_2, 7200)  # Costo estimado con los ingredientes 7200
            self.assertEqual(costo_producto_3, 7000)  # Costo estimado con los ingredientes 7000
            self.assertEqual(costo_producto_4, 6500)  # Costo estimado con los ingredientes 6500


    def test_calcular_rentabilidad(self):
        """Probar el cálculo de rentabilidad de un producto"""
        with app.app_context():
            producto_1 = Producto.query.filter(Producto.id == 1).first()
            producto_2 = Producto.query.filter(Producto.id == 2).first()
            producto_3 = Producto.query.filter(Producto.id == 3).first()
            producto_4 = Producto.query.filter(Producto.id == 4).first()
            rentabilidad_producto_1 = producto_1.calcular_rentabilidad()
            rentabilidad_producto_2 = producto_2.calcular_rentabilidad()
            rentabilidad_producto_3 = producto_3.calcular_rentabilidad()
            rentabilidad_producto_4 = producto_4.calcular_rentabilidad()

            self.assertGreater(rentabilidad_producto_1, 0)  # Rentabilidad debe ser positiva
            self.assertGreater(rentabilidad_producto_2, 0)  # Rentabilidad debe ser positiva
            self.assertGreater(rentabilidad_producto_3, 0)  # Rentabilidad debe ser positiva
            self.assertGreater(rentabilidad_producto_4, 0)  # Rentabilidad debe ser positiva


    def test_producto_mas_rentable(self):
        """Probar el producto más rentable"""
        with app.app_context():
            productos = Producto().query.all()
            ingredientes = Ingrediente().query.all()
            heladeria = Heladeria(productos, ingredientes)
            producto_mas_rentable = heladeria.producto_mas_rentable()
            self.assertEqual(producto_mas_rentable, 'Malteada Fresa') # Producto mas rentable en la heladería: Malteada Fresa

    def test_vender_producto_exitoso(self):
        """Probar si un producto se vende exitosamente"""
        with app.app_context():
                productos = Producto().query.all()
                producto_vender = Producto.query.filter(Producto.id == 3).first()
                ingredientes = Ingrediente().query.all()
                heladeria = Heladeria(productos, ingredientes)
                mensaje = heladeria.vender_producto(producto_vender.id)
                self.assertEqual(mensaje, "¡Vendido!")

    def test_vender_producto_sin_inventario(self):
        """Probar si se lanza una excepción cuando no hay inventario suficiente para vender el producto"""
        with app.app_context():
                productos = Producto().query.all()
                producto_vender = Producto.query.filter(Producto.id == 1).first() # Producto sin suficiente inventario
                ingredientes = Ingrediente().query.all()
                heladeria = Heladeria(productos, ingredientes)
                with self.assertRaises(ValueError) as context:
                    heladeria.vender_producto(producto_vender.id)
                    print(context.exception)

    def test_vender_producto_no_encontrado(self):
        """Probar si se maneja la excepción cuando el producto no se encuentra"""
        with app.app_context():
            productos = Producto().query.all()
            ingredientes = Ingrediente().query.all()
            heladeria = Heladeria(productos, ingredientes)
            mensaje = heladeria.vender_producto(4563)  # Id de producto no válido
            self.assertEqual(mensaje, "Producto no encontrado")
