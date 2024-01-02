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
afp_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@afp_router .post ('/create_afp', tags=["Instituciones AFP"],status_code=200, dependencies=[Depends(JWTBearer())])
def create_afp():
    return JSONResponse (status_code=201,content={"message":"Se creo una institución AFP en el sistema"})  

# ruta para listar las Instituciones AFP 
@afp_router .get ('/afp', tags=["Instituciones AFP"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_afp():
    return JSONResponse (status_code=201,content={"message":"Se obtuvo un listado de las instituciones AFP en el sistema"})  

# ruta para consultar una Institución AFP por Id
@afp_router .get ('/afp/{id}', tags=["Instituciones AFP"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_basic_parameter(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener una institucon AFP por ID"})  

# ruta para actualizar una institución AFP por Id
@afp_router .put ('/afp/{id}/update', tags=["Instituciones AFP"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_basic_parameter(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar una Institución AFP por ID"})      
