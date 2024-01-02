from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# creamos la Instancia de FastAPI
app = FastAPI()

# Nombre de la Aplicacion
app.title="B1 Nómina by Kyros"
# Versión de la Aplicacion
app.version="1.0"

# Ruta de inicio
@app.get ('/login', tags=["Home"])
def login():
    return HTMLResponse('Login', status_code=200)

# Rutas de Usuario
# Crear el Usuario
@app.post ('/create_users', tags=["Usuarios"])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@app.get ('/users', tags=["Usuarios"])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@app.get ('/users/{id}', tags=["Usuarios"])
def get_user(id: int):
    return f"Ver el usuario {id}"


# Actualizar el usuario representado por el ID
@app.put ('/users/{id}/update', tags=["Usuarios"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"


# -------- Rutas de Parametros Básicos ------------
# ruta para crear los Parametros Básicos
@app.post ('/create_basic_parameter', tags=["Parametros Basicos"])
def create_basic_parameter():
    return "Hello word!"


# ruta para listar los Parametros Básicos 
@app.get ('/basic_parameter', tags=["Parametros Basicos"])
def list_basic_parameters():
    return "Hello word!"


# ruta para consultar un Parametros Básicos por Id
@app.get ('/basic_parameter/{id}', tags=["Parametros Basicos"])
def get_basic_parameter(id: int):
    return f"Ver el Parametros Básicos por ID {id}"


# Actualizar el Parametros Básicos representado por el ID
@app.put ('/basic_parameter/{id}/update', tags=["Parametros Basicos"])
def update_user(id: int):
    return f"Actualizar el parametro básico por ID {id}"



# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@app.post ('/create_afp', tags=["Instituciones AFP"])
def create_afp():
    return "Hello word!"

# ruta para listar las Instituciones AFP 
@app.get ('/afp', tags=["Instituciones AFP"])
def list_afp():
    return "Hello word!"

# ruta para consultar una Institución AFP por Id
@app.get ('/afp/{id}', tags=["Instituciones AFP"])
def get_basic_parameter(id: int):
    return f"Ver la Institucion AFP por ID {id}"    

# ruta para actualizar una institución AFP por Id
@app.put ('/afp/{id}/update', tags=["Instituciones AFP"])
def get_basic_parameter(id: int):
    return f"Actualizar la Institucion AFP por ID {id}"     


# -------- Rutas Bancos ------------
# ruta para crear las Instituciones Bancaria
@app.post ('/create_banco', tags=["Bancos"])
def create_afp():
    return "Hello word!"

# ruta para listar las Instituciones Bancaria 
@app.get ('/bancos', tags=["Bancos"])
def list_afp():
    return "Hello word!"

# ruta para consultar una Institución Bancaria por Id
@app.get ('/bancos/{id}', tags=["Bancos"])
def get_basic_parameter(id: int):
    return f"Ver la Institucion AFP por ID {id}"    

# ruta para actualizar una institución Bancaria por Id
@app.put ('/bancos/{id}/update', tags=["Bancos"])
def get_basic_parameter(id: int):
    return f"Actualizar la Institucion AFP por ID {id}"   

