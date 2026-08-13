"""
Módulo de modelos SQLAlchemy.

Define la entidad Student que representa la tabla 'students'.
"""

from database import db
from datetime import date


class Student(db.Model):
    """
    Modelo que representa a un estudiante.

    Atributos:
        id: Identificador único autoincremental (clave primaria).
        name: Nombre completo del estudiante (obligatorio).
        email: Correo electrónico del estudiante (obligatorio, único).
        birth_date: Fecha de nacimiento del estudiante (opcional).
        nationality: Nacionalidad del estudiante (opcional).
        current_residence_city: Ciudad de residencia actual (opcional).
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    nationality = db.Column(db.String(80), nullable=True)
    current_residence_city = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        """
        Convierte la instancia del estudiante a un diccionario.

        Returns:
            dict: Representación del estudiante en formato JSON serializable.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "nationality": self.nationality,
            "current_residence_city": self.current_residence_city,
        }