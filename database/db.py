from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def load_models(app):
    from models.ingrediente import Ingrediente
    from models.producto import Producto
    from models.users import Users
    
    with app.app_context():
        if not Ingrediente.query.first():
                ingrediente_1 = Ingrediente(id=1, nombre="Base Vainilla", precio=3500, calorias=100, inventario=0, es_vegetariano=True, tipo="Base", sabor="Vainilla")
                ingrediente_2 = Ingrediente(id=2, nombre="Base chocolate", precio=4000, calorias=120, inventario=7.80, es_vegetariano=True, tipo="Base", sabor="Chocolate")
                ingrediente_3 = Ingrediente(id=3, nombre="Base fresa", precio=3700, calorias=100, inventario=11.60, es_vegetariano=True, tipo="Base", sabor="Fresa")
                ingrediente_4 = Ingrediente(id=4, nombre="Base Menta", precio=4200, calorias=90, inventario=11.20, es_vegetariano=True, tipo="Base", sabor="Menta")
                ingrediente_5 = Ingrediente(id=5, nombre="Chispas Choco", precio=500, calorias=50, inventario=0, es_vegetariano=True, tipo="Complemento", sabor=None)
                ingrediente_6 = Ingrediente(id=6, nombre="Trozos Galleta", precio=800, calorias=70, inventario=18, es_vegetariano=True, tipo="Complemento", sabor=None)
                ingrediente_7 = Ingrediente(id=7, nombre="Nueces Dulce", precio=1000, calorias=120, inventario=10, es_vegetariano=False, tipo="Complemento", sabor=None)
                ingrediente_8 = Ingrediente(id=8, nombre="Crema Chantilly", precio=2000, calorias=150, inventario=28, es_vegetariano=True, tipo="Complemento", sabor=None)
    
                db.session.add(ingrediente_1)
                db.session.add(ingrediente_2)
                db.session.add(ingrediente_3)
                db.session.add(ingrediente_4)
                db.session.add(ingrediente_5)
                db.session.add(ingrediente_6)
                db.session.add(ingrediente_7)
                db.session.add(ingrediente_8)
                db.session.commit()
        
        if not Producto.query.first():
                producto_1 = Producto(id=1, nombre="Copa VainilMix", precio=11000, tipo="Copa", tipo_vaso="Doble", volumen_onzas=None, ingrediente_1_id=1, ingrediente_2_id=5, ingrediente_3_id =8)
                producto_2 = Producto(id=2, nombre="Copa MentasMix", precio=12500, tipo="Copa", tipo_vaso="Sencillo", volumen_onzas=None, ingrediente_1_id=4, ingrediente_2_id=8, ingrediente_3_id =7)
                producto_3 = Producto(id=3, nombre="Malteada Choco", precio=12000, tipo="Malteada", tipo_vaso=None, volumen_onzas="8", ingrediente_1_id=2, ingrediente_2_id=7, ingrediente_3_id =8)
                producto_4 = Producto(id=4, nombre="Malteada Fresa", precio=13000, tipo="Malteada", tipo_vaso=None, volumen_onzas="12", ingrediente_1_id=3, ingrediente_2_id=6, ingrediente_3_id =8)

                db.session.add(producto_1)
                db.session.add(producto_2)
                db.session.add(producto_3)
                db.session.add(producto_4)
                db.session.commit()

        if not Users.query.first():
                user_1 = Users(id=1, username="avelandia", password="abc123..", es_admin = True, es_empleado = False )
                user_2 = Users(id=2, username="vortiz", password="def456..", es_admin= False, es_empleado = True)
                user_3 = Users(id=3, username="pperez", password="ghi789..", es_admin= False, es_empleado = False)
                db.session.add(user_1)
                db.session.add(user_2)
                db.session.add(user_3)                 
                db.session.commit()

def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        