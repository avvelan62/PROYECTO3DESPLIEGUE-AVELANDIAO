from flask_login import UserMixin, login_user, login_required, current_user
from flask import Flask, Blueprint, render_template, jsonify, request, flash, redirect, url_for
from models.users import Users 

login_blueprint = Blueprint('login_bp', __name__)


@login_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        usuario = Users.query.filter(Users.username == username).first()
        if usuario:
            es_autenticado = usuario.validar_autenticacion(username, password)
    
            if es_autenticado:
                login_user(usuario)
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('heladeria_bp.index'))
        
        flash('Usuario y contraseña incorrecta', 'error')
        return render_template("login.html")
