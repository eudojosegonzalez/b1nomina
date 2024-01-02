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
user_localization_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear los datos de contacto de un usuario
@user_localization_router.post ('/create_user_localizacion', tags=["Localizacion"],status_code=200, dependencies=[Depends(JWTBearer())])
def create_user_localization():
    return JSONResponse (status_code=201,content={"message":"Se creo un dato de contacto de un usuario"})  

# ruta para listar los datos de contacto de los usuarios
@user_localization_router.get ('/user_localizacion', tags=["Localizacion"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_user_localization():
    return JSONResponse (status_code=201,content={"message":"Se obtuvo un listadolos datos de contacto de los usuarios"})  

# ruta para consultar los datos de contacto de un usuario por el Id
@user_localization_router.get ('/user_localizacion/{id}', tags=["Localizacion"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user_localization(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener los datos de contacto de los usuarios por ID"})  

# ruta para actualizar  los datos de contacto de un usuario por el Id
@user_localization_router.put ('/user_localizacion/{id}/update', tags=["Localizacion"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_user_localization(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar los datos de contacto de los usuarios por ID"})      
