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
from schemas.bancos import Bancos as bancosSchema


# importamos el controlador 
from controller.bancos import bancosController


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
def create_banco(banco:bancosSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=bancosController(db).create_banco(banco,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newBanco=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Banco en el sistema","newBanco":jsonable_encoder(newBanco)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe un banco con este nombre, no puede volver a crearlo","Banco":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe un banco con este codigo, no puede volver a crearlo","Banco":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los bancos en el sistema
@bancos_router.get ('/list_bancos', 
tags=["Bancos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
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
def list_bancos(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = bancosController(db).list_bancos(page,records)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 

# ruta para consultar una Institución Bancaria por Id
@bancos_router.get ('/bancos/{id}', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_banco(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener un Banco por ID"})  


# ruta para actualizar una institución Bancaria por Id
@bancos_router.put ('/bancos/{id}/update', tags=["Bancos"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_banco(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar un Banco por ID"})     
