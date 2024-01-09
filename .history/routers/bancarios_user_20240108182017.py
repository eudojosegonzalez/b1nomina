'''
Rutas de Bancarios Usuarios
2024-01
'''
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
#from schemas.bancos import Bancos

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
bancarios_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancarios Usuarios ------------
# ruta para crear las Instituciones Bancaria
@bancarios_user_router.post ('/create_bancarios_user', 
tags=["Bancarios Usuarios"], 
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo el data Bancario del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el data Bancario del usuario en el sistema",
                            "newUserId":"1"
                        }
                    } 
                }       
            },
        403: {
            "description": "Forbiden",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Not authenticated"
                        }
                    } 
                }       
            }, 
        500: {
            "description": "Su session ha expirado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Su session ha expirado",
                            "estado":"Signature has expired"
                        }
                    } 
                }       
            },                
        520: {
            "description": "Ocurrió un error que no pudo ser controlado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Ocurrió un error que no pudo ser controlado",
                            "estado":"System Error"
                        }
                    } 
                }       
            },                       
    }
                             )
def create_bancarios_user(bancarioUsuario):
    return JSONResponse (status_code=201,content={"message":"Se creo un registro bancario del uuario en el sistema"})  

# ruta para listar los datos bancarios de todos los usuarios
@bancarios_user_router.get ('/list_bancarios_user', tags=["Bancarios Usuarios"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_bancarios_user():
    return JSONResponse (status_code=200,content={"message":"se Obtuvo un listado de los Bancos en el sistema"})  

# ruta para consultar los datos Bancarios de un usuario
@bancarios_user_router.get ('/bancarios_user/{id}', tags=["Bancarios Usuarios"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_bancarios_user(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener un Banco por ID"})  

# ruta para consultar el historial de los datos  Bancarios de un usuario
@bancarios_user_router.get ('/bancarios_user/{id}/list_historicos', tags=["Bancarios Usuarios"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_bancarios_user(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener un Banco por ID"})  


# ruta para actualizar los datos Bancarios de un Usuario
@bancarios_user_router.put ('/bancarios_user/{id}/update', tags=["Bancarios Usuarios"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_bancarios_user(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar un Banco por ID"})     