from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# creamos la Instancia de FastAPI
app = FastAPI()

# Nombre de la Aplicacion
app.title="B1 Nómina"
# Versión de la Aplicacion
app.version="1.0"

# Ruta de inicio
@app.get ('/login', tags=["Home"])
def login():
    return HTMLResponse('Login', status_code=200)

# Rutas de Usuario
# Crear el Usuario
@app.post ('/create_users', tags=["Users"])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@app.get ('/users', tags=["Users"])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@app.get ('/users/{id}', tags=["Users"])
def get_user(id: int):
    return f"Ver el usuario {id}"


# Listar ver el representado por el ID
@app.put ('/users/{id}/update', tags=["Users"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"


