from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
from schemas.user import User

#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objketos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
bancos_router = APIRouter()

# -------- Rutas Bancos ------------
# ruta para crear las Instituciones Bancaria
@bancos_router.post ('/create_banco', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def create_afp():
    return "Hello word!"

# ruta para listar las Instituciones Bancaria 
@bancos_router.get ('/bancos', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_afp():
    return "Hello word!"

# ruta para consultar una Institución Bancaria por Id
@bancos_router.get ('/bancos/{id}', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_basic_parameter(id: int):
    return f"Ver la Institucion AFP por ID {id}"    

# ruta para actualizar una institución Bancaria por Id
@bancos_router.put ('/bancos/{id}/update', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_basic_parameter(id: int):
    return f"Actualizar la Institucion AFP por ID {id}"   
