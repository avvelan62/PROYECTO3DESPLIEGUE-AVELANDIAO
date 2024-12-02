from flask import Flask, redirect, url_for
from flask_login import LoginManager 
from dotenv import load_dotenv
from database.db import db, init_db, load_models
from controllers.heladeria_controller import heladeria_blueprint
from controllers.login_controller import login_blueprint
from controllers.heladeria_api_controller import heladeria_api_blueprint
from models.users import Users
import os

load_dotenv(override=True)
app = Flask(__name__, template_folder="views")
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager(app)
db.init_app(app)
init_db(app) # Comentar para entorno de producción
load_models(app)

app.register_blueprint(heladeria_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(heladeria_api_blueprint)


# Redirigir la raíz al blueprint
@app.route('/')
def home():
    return redirect(url_for('login_bp.login')) 

@login_manager.user_loader
def load_user(user_id: int):
    """Conocer si el usuario esta logueado

    Args:
        user_id (int): Identificador del usuario

    """
    return Users.query.get(int(user_id))