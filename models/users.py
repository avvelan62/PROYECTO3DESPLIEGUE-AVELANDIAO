from database.db import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    es_admin = db.Column(db.Boolean(), nullable = False)
    es_empleado = db.Column(db.Boolean(), nullable = False)

    def validar_autenticacion(self, username: str, password: str) -> bool:
        """Valida la autenticación del usuario

        Returns:
            bool: Resultado de la operación
        """
        if self.username == username and self.password == password:
            return True
        else:
            return False
        