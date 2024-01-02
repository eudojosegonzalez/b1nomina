from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from config.database import engine, Base
#from schemas.user import Bancos

#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objketos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
basic_parameter_router = APIRouter(prefix="/V1.0")

# -------- Rutas de Parametros Básicos ------------
# ruta para crear los Parametros Básicos
@basic_parameter_router.post ('/create_basic_parameter', tags=["Parametros Basicos"],status_code=200, dependencies=[Depends(JWTBearer())])
def create_basic_parameter():
    return JSONResponse (status_code=201,content={"message":"Se creo un Parámetro Básico en el sistema"})  


# ruta para listar los Parametros Básicos 
@basic_parameter_router.get ('/basic_parameter', tags=["Parametros Basicos"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_basic_parameters():
    return JSONResponse (status_code=201,content={"message":"Se obtuvo un loistado de Parámetros Básicos en el sistema"})  


# ruta para consultar un Parametros Básicos por Id
@basic_parameter_router.get ('/basic_parameter/{id}', tags=["Parametros Basicos"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_basic_parameter(id: int):
    return JSONResponse (status_code=201,content={"message":"Se obtuvo un Parámetro Básico en el sistema en base a un ID"})  


# Actualizar el Parametros Básicos representado por el ID
@basic_parameter_router.put ('/basic_parameter/{id}/update', tags=["Parametros Basicos"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_basic_parameter(id: int):
    return JSONResponse (status_code=201,content={"message":"Se actualizó un Parámetro Básico en el sistema en base a un ID"})  
        
