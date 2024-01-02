from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse


# esta variable define al router
bancos_router = APIRouter()

# -------- Rutas Bancos ------------
# ruta para crear las Instituciones Bancaria
@bancos_router.post ('/create_banco', tags=["Bancos"])
def create_afp():
    return "Hello word!"

# ruta para listar las Instituciones Bancaria 
@bancos_router.get ('/bancos', tags=["Bancos"])
def list_afp():
    return "Hello word!"

# ruta para consultar una Institución Bancaria por Id
@bancos_router.get ('/bancos/{id}', tags=["Bancos"])
def get_basic_parameter(id: int):
    return f"Ver la Institucion AFP por ID {id}"    

# ruta para actualizar una institución Bancaria por Id
@bancos_router.put ('/bancos/{id}/update', tags=["Bancos"])
def get_basic_parameter(id: int):
    return f"Actualizar la Institucion AFP por ID {id}"   
