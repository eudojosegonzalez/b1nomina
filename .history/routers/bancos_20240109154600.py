'''
Rutas de Bancos
2024-01
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv

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
from schemas.bancos import Bancos


# importamos el controlador 
from controller.bancos import Ba


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
bancos_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancos ------------
# ruta para crear las Instituciones Bancaria
@bancos_router.post ('/create_banco', 
tags=["Bancos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Banco en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Banco en el sistema",
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
def create_banco():
    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})            

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
