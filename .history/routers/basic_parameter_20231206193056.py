from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
'''from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
from schemas.user import User'''

# esta variable define al router
basic_parameter_router = APIRouter()

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
        
