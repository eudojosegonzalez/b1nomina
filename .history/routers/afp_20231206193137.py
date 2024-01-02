from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
'''from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
from schemas.user import User'''

# esta variable define al router
afp_router = APIRouter()

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
