from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
#from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base

#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token

#importamos el banco
from schemas.user import Bancos

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
bancos_router = APIRouter()

# -------- Rutas Bancos ------------
# ruta para crear las Instituciones Bancaria
@bancos_router.post ('/create_banco', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def create_banco():
    return JSONResponse (status_code=201,content={"message":"Se creo un banco en el sistema"})  

# ruta para listar las Instituciones AFP
@bancos_router.get ('/bancos', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_bancos():
    return JSONResponse (status_code=200,content={"message":"se Obtuvo un listado de los Bancos en el sistema"})  

# ruta para consultar una Institución Bancaria por Id
@bancos_router.get ('/bancos/{id}', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_banco(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener un Banco por ID"})  


# ruta para actualizar una institución Bancaria por Id
@bancos_router.put ('/bancos/{id}/update', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_banco(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar un Banco por ID"})     
