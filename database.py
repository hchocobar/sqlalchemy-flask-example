"""
Módulo de configuración de base de datos.

Configura la conexión a SQLite usando SQLAlchemy.
Provee la instancia de SQLAlchemy y la función init_db()
para crear las tablas en la base de datos.
"""

from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """
    Inicializa la base de datos y crea las tablas si no existen.

    Args:
        app: Instancia de la aplicación Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()