from flask import Blueprint, render_template, request, redirect, url_for
from models.ingrediente import Ingrediente
from models.producto import Producto
from models.heladeria import Heladeria
from flask_login import login_required


heladeria_blueprint = Blueprint('heladeria_bp', __name__, url_prefix="/heladeria")

@heladeria_blueprint.route('/')
@login_required
def index():
    return render_template("index.html")


@heladeria_blueprint.route('/ingredientes')
@login_required
def ingredientes():
    ingrediente_base = Ingrediente.query.filter(Ingrediente.tipo == "Base").all()
    ingrediente_complemento = Ingrediente.query.filter(Ingrediente.tipo == "Complemento").all()
    for base in ingrediente_base:
        base.es_sano = base.es_sano()
    for complemento in ingrediente_complemento:
        complemento.es_sano = complemento.es_sano()
            
    lista_ingredientes = [ingrediente_base, ingrediente_complemento]
    return render_template("ingredientes.html", lista_ingredientes = lista_ingredientes)


@heladeria_blueprint.route('/ingredientes/abastecer', methods=['POST'])
@login_required
def abastecer_ingrediente():
    ingrediente_id = request.form['ingrediente_id']
    ingrediente_abastecer = Ingrediente.query.get(ingrediente_id)
    
    if ingrediente_abastecer:
        ingrediente_abastecer.abastecer()
        print("Ingrediente abastecido exitosamente.")
    else:
        print("Ingrediente no encontrado.")
    
    return redirect(url_for('heladeria_bp.ingredientes'))


@heladeria_blueprint.route('/ingredientes/renovar', methods=['POST'])
@login_required
def renovar_inventario():
    ingrediente_id = request.form['ingrediente_id']
    ingrediente_renovar = Ingrediente.query.get(ingrediente_id)
    
    if ingrediente_renovar:
        ingrediente_renovar.renovar_inventario()
        print("Ingrediente renovado exitosamente.")
    else:
        print("Ingrediente no encontrado.")
    
    return redirect(url_for('heladeria_bp.ingredientes'))


@heladeria_blueprint.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    productos = Producto().query.all()
    ingredientes = Ingrediente().query.all()
    heladeria = Heladeria(productos, ingredientes)
    
    ingredientes_disponibles = Producto()
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        ingredientes_disponibles = Producto.query.get(producto_id)
    
    producto_copa = Producto.query.filter(Producto.tipo == "Copa").all()
    producto_malteada = Producto.query.filter(Producto.tipo == "Malteada").all()
    
    for copa in producto_copa:
        copa.calorias = copa.calcular_calorias()
        copa.costo_produccion = copa.calcular_costo()
        copa.rentabilidad = copa.calcular_rentabilidad()
    
    for malteada in producto_malteada:
        malteada.calorias = malteada.calcular_calorias()
        malteada.costo_produccion = malteada.calcular_costo()
        malteada.rentabilidad = malteada.calcular_rentabilidad()
  
    producto_mas_rentable = heladeria.producto_mas_rentable()
    lista_productos = [producto_copa, producto_malteada]
    return render_template("productos.html", lista_productos=lista_productos, ingredientes_disponibles = ingredientes_disponibles, producto_mas_rentable = producto_mas_rentable )
   
    
@heladeria_blueprint.route('/productos/vender', methods=['POST'])
@login_required
def vender_producto():    
    productos = Producto().query.all()
    ingredientes = Ingrediente().query.all()
    heladeria = Heladeria(productos, ingredientes)
    
    producto_id = request.form['producto_id']
    if producto_id:
        producto = Producto.query.get(producto_id)
        if producto:
            try:
                vendido = heladeria.vender_producto(producto_id)
                print(vendido)
            except ValueError as e:     
                print(f"¡Oh no! Nos hemos quedado sin {e}")
        else:
            print("Producto no encontrado.")
    else:
        print("No se proporcionó un ID de producto.")

    return redirect(url_for('heladeria_bp.productos'))
