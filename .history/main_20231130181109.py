from fastapi import FastAPI

# creamos la Instancia de FastAPI
app = FastAPI()

# Nombre de la Aplicacion
app.title="B1 Nómina"
# Versión de la Aplicacion
app.version="1.0"

# Ruta de inicio
@app.get ('/login', tags=["Home"])
def login():
    return "Hello word!"

# Rutas de Usuario
# Crear el Usuario
@app.get ('/create_users', tags=["Users"])
def createUser():
    return "Hello word!"


# Listar todos los usuarios del sistema
@app.get ('/users', tags=["Users"])
def listUser():
    return "Hello word!"

# Listar ver el representado por el ID
@app.get ('/users/{id}/', tags=["Users"])
def viewUser():
    return "Hello word!"

# Listar ver el representado por el ID
@app.get ('/users/{id}/update', tags=["Users"])
def updateUser():
    return "Hello word!"

