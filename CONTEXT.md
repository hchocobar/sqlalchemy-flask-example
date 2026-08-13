# CONTEXT.md

## Objetivo del proyecto

Crear una API REST con **Flask**, **SQLite** y **SQLAlchemy** para gestionar registros de estudiantes mediante operaciones CRUD.

La API debe permitir:

- Crear estudiantes
- Consultar estudiantes
- Consultar un estudiante por su identificador
- Actualizar estudiantes
- Eliminar estudiantes

El proyecto debe mantener una estructura simple, clara y adecuada para fines educativos.

---

## Reglas de idioma

Este proyecto debe seguir las siguientes reglas de idioma:

- Los nombres de tablas deben estar en **inglés**.
- Los nombres de campos deben estar en **inglés**.
- Los nombres de endpoints deben estar en **inglés**.
- Los nombres de variables, clases y funciones pueden estar en **inglés** para mantener consistencia técnica.
- Los datos de ejemplo deben estar en **español**.
- Los mensajes de respuesta de la API deben estar en **español**.
- Los comentarios dentro del código deben estar en **español**.

Ejemplos:
```python
# Comentario en español
student = Student(name="Ana Torres", nationality="Colombiana")
```
Endpoint válido:
```text
GET /students
```
Mensaje válido:
```json
{
  "message": "Estudiante encontrado correctamente"
}
```
---

## Entidad principal

La entidad principal del sistema es `Student`.

Debe estar asociada a una tabla llamada:
```text
students
```
### Campos de la tabla `students`

| Campo | Tipo sugerido | Requerido | Descripción                                 |
|---|---:|----------:|---------------------------------------------|
| `id` | Integer |        Sí | Identificador único autoincremental         |
| `name` | String |        Sí | Nombre completo del estudiante              |
| `email` | String |        Sí | Correo electrónico del estudiante |
| `birth_date` | Date |        No | Fecha de nacimiento del estudiante          |
| `nationality` | String |        No | Nacionalidad del estudiante                 |
| `current_residence_city` | String |        No | Ciudad de residencia actual                 |

### Restricciones recomendadas

- `id` debe ser clave primaria.
- `email` debe ser único.
- `name` no debe estar vacío.
- `email` debe tener formato válido.
- `birth_date` debe usar formato `YYYY-MM-DD`.

---

## Modelo esperado

El modelo SQLAlchemy debe llamarse:
```text
Student
```
Debe representar la tabla:
```text
students
```
Campos sugeridos:
```python
id
name
email
birth_date
nationality
current_residence_city
```
---

## Endpoints requeridos

La API debe exponer endpoints REST usando nombres en inglés.

### Crear estudiante
```http
POST /students
```
Body esperado:
```json
{
  "name": "María Fernanda López",
  "email": "maria.lopez@example.com",
  "birth_date": "2001-04-15",
  "nationality": "Colombiana",
  "current_residence_city": "Medellín"
}
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiante creado correctamente",
  "student": {
    "id": 1,
    "name": "María Fernanda López",
    "email": "maria.lopez@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Medellín"
  }
}
```
Código HTTP sugerido:
```text
201 Created
```
---

### Listar estudiantes
```http
GET /students
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiantes obtenidos correctamente",
  "students": [
    {
      "id": 1,
      "name": "María Fernanda López",
      "email": "maria.lopez@example.com",
      "birth_date": "2001-04-15",
      "nationality": "Colombiana",
      "current_residence_city": "Medellín"
    }
  ]
}
```
Código HTTP sugerido:
```text
200 OK
```
---

### Obtener estudiante por ID
```http
GET /students/<id>
```
Ejemplo:
```http
GET /students/1
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiante encontrado correctamente",
  "student": {
    "id": 1,
    "name": "María Fernanda López",
    "email": "maria.lopez@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Medellín"
  }
}
```
Si el estudiante no existe:
```json
{
  "message": "Estudiante no encontrado"
}
```
Código HTTP sugerido:
```text
404 Not Found
```
---

### Actualizar estudiante
```http
PUT /students/<id>
```
Ejemplo:
```http
PUT /students/1
```
Body esperado:
```json
{
  "name": "María Fernanda López Gómez",
  "email": "maria.fernanda@example.com",
  "birth_date": "2001-04-15",
  "nationality": "Colombiana",
  "current_residence_city": "Bogotá"
}
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiante actualizado correctamente",
  "student": {
    "id": 1,
    "name": "María Fernanda López Gómez",
    "email": "maria.fernanda@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Bogotá"
  }
}
```
Código HTTP sugerido:
```text
200 OK
```
Si el estudiante no existe:
```json
{
  "message": "Estudiante no encontrado"
}
```
Código HTTP sugerido:
```text
404 Not Found
```
---

### Actualizar parcialmente estudiante

Opcional, pero recomendado:
```http
PATCH /students/<id>
```
Ejemplo:
```http
PATCH /students/1
```
Body esperado:
```json
{
  "current_residence_city": "Cali"
}
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiante actualizado correctamente",
  "student": {
    "id": 1,
    "name": "María Fernanda López Gómez",
    "email": "maria.fernanda@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Cali"
  }
}
```
Código HTTP sugerido:
```text
200 OK
```
---

### Eliminar estudiante
```http
DELETE /students/<id>
```
Ejemplo:
```http
DELETE /students/1
```
Respuesta exitosa sugerida:
```json
{
  "message": "Estudiante eliminado correctamente"
}
```
Código HTTP sugerido:
```text
200 OK
```
Si el estudiante no existe:
```json
{
  "message": "Estudiante no encontrado"
}
```
Código HTTP sugerido:
```text
404 Not Found
```
---

## Validaciones requeridas

La API debe validar los datos recibidos antes de crear o actualizar registros.

### Validaciones mínimas

- `name` es obligatorio.
- `email` es obligatorio.
- `email` debe tener un formato válido.
- `email` no debe repetirse en otro estudiante.
- `birth_date` no es obligatorio.
- `birth_date` debe tener formato `YYYY-MM-DD`.
- `nationality` no es obligatoria.
- `current_residence_city` no es obligatoria.

### Respuesta sugerida para errores de validación
```json
{
  "message": "Los datos enviados no son válidos",
  "errors": {
    "email": "El correo electrónico es obligatorio",
    "birth_date": "La fecha de nacimiento debe tener formato YYYY-MM-DD"
  }
}
```
Código HTTP sugerido:
```text
400 Bad Request
```
---

## Manejo de errores

La API debe responder siempre en formato JSON.

### Error por recurso no encontrado
```json
{
  "message": "Estudiante no encontrado"
}
```
Código HTTP:
```text
404 Not Found
```
### Error por email duplicado
```json
{
  "message": "El correo electrónico ya está registrado"
}
```
Código HTTP sugerido:
```text
409 Conflict
```
### Error interno
```json
{
  "message": "Ocurrió un error interno en el servidor"
}
```
Código HTTP:
```text
500 Internal Server Error
```
---

## Estructura sugerida del proyecto
```text
sqlalchemy-flask-example/
├── app.py
├── models.py
├── database.py
├── requirements.txt
├── README.md
└── CONTEXT.md
```
### Responsabilidades sugeridas

#### `app.py`

Debe contener:

- Creación de la aplicación Flask.
- Registro de endpoints.
- Manejo de request y response.
- Validaciones principales o uso de funciones auxiliares.

#### `models.py`

Debe contener:

- Definición del modelo `Student`.
- Método para convertir un estudiante a diccionario, por ejemplo `to_dict`.

#### `database.py`

Debe contener:

- Configuración de SQLite.
- Inicialización de SQLAlchemy.
- Función para crear las tablas.

#### `requirements.txt`

Debe incluir, como mínimo:
```text
Flask
Flask-SQLAlchemy
```
---

## Configuración de base de datos

La base de datos debe ser SQLite.

Nombre sugerido del archivo:
```text
students.db
```
URI sugerida:
```text
sqlite:///students.db
```
La aplicación debe crear la tabla `students` si no existe.

---

## Formato de fechas

El campo `birth_date` debe recibirse y devolverse en formato:
```text
YYYY-MM-DD
```
Ejemplo:
```text
2001-04-15
```
Internamente puede almacenarse como `Date` usando SQLAlchemy.

---

## Serialización esperada

El modelo `Student` debe poder convertirse a JSON con una estructura como esta:
```json
{
  "id": 1,
  "name": "María Fernanda López",
  "email": "maria.lopez@example.com",
  "birth_date": "2001-04-15",
  "nationality": "Colombiana",
  "current_residence_city": "Medellín"
}
```
---

## Datos de ejemplo

Los datos de ejemplo deben estar en español.
```json
[
  {
    "name": "Ana Martínez",
    "email": "ana.martinez@example.com",
    "birth_date": "2000-02-10",
    "nationality": "Argentina",
    "current_residence_city": "Buenos Aires"
  },
  {
    "name": "Carlos Ramírez",
    "email": "carlos.ramirez@example.com",
    "birth_date": "1999-08-21",
    "nationality": "Mexicana",
    "current_residence_city": "Ciudad de México"
  },
  {
    "name": "Lucía Fernández",
    "email": "lucia.fernandez@example.com",
    "birth_date": "2002-11-05",
    "nationality": "Chilena",
    "current_residence_city": "Santiago"
  }
]
```
---

## Criterios de aceptación

El CRUD se considerará completo cuando:

- Exista el modelo `Student`.
- Exista la tabla `students`.
- La API permita crear estudiantes con `POST /students`.
- La API permita listar estudiantes con `GET /students`.
- La API permita consultar un estudiante con `GET /students/<id>`.
- La API permita actualizar un estudiante con `PUT /students/<id>`.
- La API permita eliminar un estudiante con `DELETE /students/<id>`.
- Las respuestas sean JSON.
- Los mensajes estén en español.
- Los endpoints y campos estén en inglés.
- Se validen los campos obligatorios.
- Se controle el caso de estudiante no encontrado.
- Se controle el caso de correo electrónico duplicado.
- La base de datos SQLite funcione correctamente.

---

## Convenciones recomendadas

- Usar nombres en inglés para rutas, modelos, atributos y columnas.
- Usar comentarios en español para explicar partes importantes del código.
- Usar mensajes claros en español para respuestas de la API.
- Mantener respuestas consistentes usando las claves:
  - `message`
  - `student`
  - `students`
  - `errors`
- Evitar lógica compleja innecesaria.
- Priorizar claridad sobre abstracción excesiva.

---

## Ejemplos de pruebas manuales con curl

### Crear estudiante
```bash
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María Fernanda López",
    "email": "maria.lopez@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Medellín"
  }'
```
### Listar estudiantes
```bash
curl http://localhost:5000/students
```
### Obtener estudiante por ID
```bash
curl http://localhost:5000/students/1
```
### Actualizar estudiante
```bash
curl -X PUT http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María Fernanda López Gómez",
    "email": "maria.fernanda@example.com",
    "birth_date": "2001-04-15",
    "nationality": "Colombiana",
    "current_residence_city": "Bogotá"
  }'
```
### Eliminar estudiante
```bash
curl -X DELETE http://localhost:5000/students/1
```
