from flask import jsonify, Blueprint, render_template, redirect, url_for
from models.ingrediente import Ingrediente, IngredienteSchema
from models.producto import Producto, ProductoSchema
from models.heladeria import Heladeria
from flask_login import login_required, current_user

heladeria_api_blueprint = Blueprint('heladeria_api_bp', __name__, url_prefix="/api/v1/heladeria")


@heladeria_api_blueprint.route('/no_autorizado')
def ruta_no_autorizada():
    return render_template("no_autorizado.html"), 403


@heladeria_api_blueprint.route('/productos')
def obtener_productos():
    """
    Obtiene todos los productos de la heladería.
    Returns:
        Response:
            - 200: Operación exitosa.
    """
    producto_schema = ProductoSchema(many=True)
    productos = Producto.query.all()
    return jsonify(producto_schema.dump(productos)), 200


@heladeria_api_blueprint.route('/productos/<int:id>', methods=['GET'])
@login_required
def obtener_producto_id(id):
    """
    Obtiene el producto de la heladería según su ID.
    Args:
        id (int): ID único del producto a consultar.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        producto_schema = ProductoSchema()
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(producto_schema.dump(producto)), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))

 
@heladeria_api_blueprint.route('/productos/<string:nombre>', methods=['GET'])
@login_required
def obtener_producto_nombre(nombre):
    """
    Obtiene el producto de la heladería según su nombre.
    Args:
        nombre (str): Nombre del producto a consultar.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        producto_schema = ProductoSchema()
        producto = Producto.query.filter(Producto.nombre == nombre).first()
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(producto_schema.dump(producto)), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))
   
 
@heladeria_api_blueprint.route('/productos/calorias/<int:id>', methods=['GET'])
@login_required
def obtener_producto_calorias(id):
    """
    Obtiene las calorías de un producto según su ID
    Args:
        id (int): ID único del producto a consultar calorías.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated:
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify({"id": producto.id, "producto": producto.nombre, "calorias": producto.calcular_calorias()}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/productos/rentabilidad/<int:id>', methods=['GET'])
@login_required
def obtener_producto_rentabilidad(id):
    """
    Args:
        id (int): ID único del producto a consultar rentabilidad.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Producto no encontrado.
    """
    if  current_user.is_authenticated and current_user.es_admin:
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify({"id": producto.id, "producto": producto.nombre, "rentabilidad": producto.calcular_rentabilidad()}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/productos/costo/<int:id>', methods=['GET'])
@login_required
def obtener_producto_costo(id):
    """
    Obtiene la rentabilidad de un producto según su ID
    Args:
        id (int): ID único del producto a consultar costo de producción.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Producto no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify({"id": producto.id, "producto": producto.nombre, "costo": producto.calcular_costo()}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/productos/vender/<int:id>', methods=['GET', 'POST'])
@login_required
def vender_producto(id):
    """
    Vender un producto según su ID
    Args:
        id (int): ID único del producto a vender.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Producto no encontrado.
    """
    if  current_user.is_authenticated:
        productos = Producto().query.all()
        ingredientes = Ingrediente().query.all()
        heladeria = Heladeria(productos, ingredientes)
    
        producto = Producto.query.get(id)
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
    
        try:
            vendido = heladeria.vender_producto(producto.id)
        except ValueError as e:     
            vendido = (f"¡Oh no! Nos hemos quedado sin {e}")
    
        return jsonify({"id": producto.id, "producto": producto.nombre, "mensaje": vendido}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes')
@login_required
def obtener_ingredientes():
    """
    Obtiene todos los ingredientes de la heladería.
    
    Returns:
        Response:
            - 200: Operación exitosa.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente_schema = IngredienteSchema(many=True)
        ingredientes = Ingrediente.query.all()
        return jsonify(ingrediente_schema.dump(ingredientes)), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes/<int:id>', methods=['GET'])
@login_required
def obtener_ingrediente_id(id):
    """
    Obtiene el ingrediente de la heladería según su ID.
    Args:
        id (int): ID único del ingrediente a consultar.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente_schema = IngredienteSchema()
        ingrediente = Ingrediente.query.get(id)
        if ingrediente is None:
            return jsonify({"error": "Ingrediente no encontrado"}), 404
    
        return jsonify(ingrediente_schema.dump(ingrediente)), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes/<string:nombre>', methods=['GET'])
@login_required
def obtener_ingrediente_nombre(nombre):
    """
    Obtiene el ingrediente de la heladería según su nombre.
    Args:
        nombre (str): Nombre del ingrediente a consultar.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente_schema = IngredienteSchema()
        ingrediente = Ingrediente.query.filter(Ingrediente.nombre == nombre).first()
        if ingrediente is None:
            return jsonify({"error": "Ingrediente no encontrado"}), 404
    
        return jsonify(ingrediente_schema.dump(ingrediente)), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes/es_sano/<int:id>', methods=['GET'])
@login_required
def obtener_ingrediente_es_sano(id):
    """
    Obtiene si el ingrediente de la heladería es sano según su id.
    Args:
        id (int): ID único del ingrediente a reabastecer.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente = Ingrediente.query.get(id)
        if ingrediente is None:
            return jsonify({"error": "Ingrediente no encontrado"}), 404

        return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "es_sano": ingrediente.es_sano()}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes/abastecer/<int:id>', methods=['GET','POST'])
@login_required
def abastecer_ingrediente(id):
    """
    Reabastece el inventario de un ingrediente de la heladería según su ID.

    Args:
        id (int): ID único del ingrediente a reabastecer.

    Returns:
        Response:
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.   
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente = Ingrediente.query.get(id)

        if ingrediente is None:
            return jsonify({"error": "Ingrediente no encontrado"}), 404

        ingrediente.abastecer()

        return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "inventario": ingrediente.inventario, "tipo": ingrediente.tipo}), 201
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))


@heladeria_api_blueprint.route('/ingredientes/renovar/<int:id>', methods=['GET','POST'])
@login_required
def renovar_inventario(id):
    """
    Renueva el inventario de un ingrediente de tipo "Complemento".

    Args:
        id (int): ID del ingrediente.

    Returns:
        Response: 
            - 200: Operación exitosa.
            - 404: Ingrediente no encontrado.
    """
    if  current_user.is_authenticated and (current_user.es_admin or current_user.es_empleado):
        ingrediente = Ingrediente.query.get(id)

        if ingrediente is None:
            return jsonify({"error": "Ingrediente no encontrado"}), 404

        if  ingrediente.tipo != "Complemento":
            return jsonify({"mensaje": "Ingrediente no es de tipo Complemento"}), 200

        ingrediente.renovar_inventario()

        return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "inventario": ingrediente.inventario, "tipo": ingrediente.tipo}), 200
    return redirect(url_for('heladeria_api_bp.ruta_no_autorizada'))
