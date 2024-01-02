from fastapi import FastAPI

# creamos la Instancia de FastAPI
app = FastAPI()

# Ruta de inicio
@app.get ('/')
def login():
    return "Hello word!"

