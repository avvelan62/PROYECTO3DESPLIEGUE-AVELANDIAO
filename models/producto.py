from database.db import db
from funciones import *
from marshmallow import schema, fields


class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(120), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    tipo = db.Column(db.String(45), nullable = False)
    tipo_vaso = db.Column(db.String(45), nullable = True)
    volumen_onzas = db.Column(db.String(45), nullable = True)

    # Claves foráneas
    ingrediente_1_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente_2_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente_3_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)

    # Relaciones
    ingrediente_1 = db.relationship('Ingrediente', foreign_keys=[ingrediente_1_id])
    ingrediente_2 = db.relationship('Ingrediente', foreign_keys=[ingrediente_2_id])
    ingrediente_3 = db.relationship('Ingrediente', foreign_keys=[ingrediente_3_id])

    # Métodos
    def calcular_costo(self) -> float:
        """Calcula es costo de producción de un producto

        Returns:
            float: Resultado de la operación
        """
        ingrediente_uno = {"precio": self.ingrediente_1.precio}
        ingrediente_dos = {"precio": self.ingrediente_2.precio}
        ingrediente_tres = {"precio": self.ingrediente_3.precio}
        return calcular_costo(ingrediente_uno, ingrediente_dos, ingrediente_tres)

    def calcular_calorias(self)-> float:
        """Calcula las calorias de un producto
        
        Returns:
            float: Resultado de la operación        
        """
        lista_calorias = [self.ingrediente_1.calorias, self.ingrediente_2.calorias, self.ingrediente_3.calorias]
        return calcular_calorias_producto(lista_calorias)

    def calcular_rentabilidad(self) -> float:
        """Calcula la rentabilidad de un producto

        Returns:
            float: Resultado de la operación
        """
        ingrediente_uno = {"precio": self.ingrediente_1.precio}
        ingrediente_dos = {"precio": self.ingrediente_2.precio}
        ingrediente_tres = {"precio": self.ingrediente_3.precio}
        return calcular_rentabilidad(self.precio, ingrediente_uno, ingrediente_dos, ingrediente_tres)


class ProductoSchema(schema.Schema):
    id = fields.Int(dump_only = True)
    nombre = fields.Str()
    precio = fields.Int()
    tipo = fields.Str()
    tipo_vaso = fields.Str()
    volumen_onzas = fields.Str()
    ingrediente_1_id = fields.Int()
    ingrediente_2_id = fields.Int()
    ingrediente_3_id = fields.Int()