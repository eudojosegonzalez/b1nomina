from fastapi import FastAPI

# creamos la Instancia de FastAPI
app = FastAPI()

# Ruta de inicio
@app.get ('/login')
def login():
    return "Hello word!"

# Rutas de Usuario
# Crear el Usuario
@app.get ('/create_users')
def createUser():
    return "Hello word!"


# Listar todos los usuarios del sistema
@app.get ('/users')
def listUser():
    return "Hello word!"

# Listar ver el representado por el ID
@app.get ('/users/{id}/')
def viewUser():
    return "Hello word!"

# Listar ver el representado por el ID
@app.get ('/users/{id}/update')
def updateUser():
    return "Hello word!"

