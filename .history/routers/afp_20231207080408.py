from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse


# esta variable define al router
afp_router = APIRouter()

# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@afp_router .post ('/create_afp', tags=["Instituciones AFP"])
def create_afp():
    return "Hello word!"

# ruta para listar las Instituciones AFP 
@afp_router .get ('/afp', tags=["Instituciones AFP"])
def list_afp():
    return "Hello word!"

# ruta para consultar una Institución AFP por Id
@afp_router .get ('/afp/{id}', tags=["Instituciones AFP"])
def get_basic_parameter(id: int):
    return f"Ver la Institucion AFP por ID {id}"    

# ruta para actualizar una institución AFP por Id
@afp_router .put ('/afp/{id}/update', tags=["Instituciones AFP"])
def get_basic_parameter(id: int):
    return f"Actualizar la Institucion AFP por ID {id}"     
