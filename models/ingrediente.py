from database.db import db
from funciones import *
from decimal import Decimal
from marshmallow import schema, fields

class Ingrediente(db.Model):
    __tablename__ = "ingredientes"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(120), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    calorias = db.Column(db.Numeric(6,2), nullable = False)
    inventario = db.Column(db.Numeric(6,2), nullable = False)
    es_vegetariano = db.Column(db.Boolean, nullable= False)
    tipo = db.Column(db.String(45), nullable = False)
    sabor = db.Column(db.String(120), nullable = True)
    
    # Métodos
    def es_sano(self) -> bool:
        """Valida si el ingrediente es sano o no
        Returns:
            bool: Resultado de la operación
        """
        return es_sano(self.calorias, self.es_vegetariano)

    def abastecer(self) -> None:
        """Abastece el ingrediente indicado
        """
        if self.tipo == "Base":
            self.inventario += Decimal(5)
        if self.tipo == "Complemento":
           self.inventario += Decimal(10)
        db.session.commit()
                  
    def renovar_inventario(self) -> None:
        """Renueva el inventario para los ingredientes complementos
        """
        if self.tipo == "Complemento":
            self.inventario = 0
        db.session.commit()

class IngredienteSchema(schema.Schema):
    id = fields.Int(dump_only = True)
    nombre = fields.Str()
    precio = fields.Int()
    calorias = fields.Decimal()
    inventario = fields.Decimal()
    es_vegetariano = fields.Bool()
    tipo = fields.Str()
    sabor = fields.Str()
