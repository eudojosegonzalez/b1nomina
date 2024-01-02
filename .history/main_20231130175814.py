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
def login():
    return "Hello word!"


# Listar los usuarios del sistema
@app.get ('/users')
def login():
    return "Hello word!"

# Listar ver el represamntado por el ID
@app.get ('/users/{id}/')
def login():
    return "Hello word!"

