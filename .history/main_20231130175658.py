from fastapi import FastAPI

# creamos la Instancia de FastAPI
app = FastAPI()

# Ruta de inicio
@app.get ('/login')
def login():
    return "Hello word!"

# Rutas de Usuario
@app.get ('/create_user')
def login():
    return "Hello word!"

