'''
Rutas de contactoto de usuario
created date: 2023-12
'''
from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta


#from typing import  Optional, List
from typing import  List
# importamos desde la configuracion de la Base de datos las clases
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder


#importamos la libreria para generar el token y validarlo
import jwt 
from utils.jwt_managr import create_token,validate_token


# importamos el controlador 
from controller.contact_users import contactUserController


# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password,verify_password


# esto importa la tabla desde la definiciones de modelos
from models.contacto import Contacto as ContactoModel
#importamos el esquema de datos para utilizarlo como referencia de datos a la hora de capturar data
from schemas.contact_user import ContactUser as ContactUserSchema


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session


# esta variable define al router
user_contact_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear los datos de contacto de un usuario
@user_contact_router.post ('/create_user_contact', 
tags=["Contacto"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo el contacto del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el contacto del usuario en el sistema",
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
            "description": "Ya existen los datos de contacto de este usuario, no puede volver a crearlos",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Ya existen los datos de contacto de este usuario, no puede volver a crearlos",
                            "estado":"Record found"
                        }
                    } 
                }       
            },                      
        501: {
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
def create_user_contact(userCreatorId:int,contactUserSchema:ContactUserSchema)->dict:
    db = Session()
    result=contactUserController(db).create_contact_user(userCreatorId,contactUserSchema)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newContactUserId=result["newContactUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el contacto del usuario en el sistema","newUserId":newContactUserId})     
    elif (estado=="-2"):
        return JSONResponse (status_code=500,content={"message":"Ya existen los datos de contacto de este usuario, no puede volver a crearlos","estado":result})    
    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})              



# ruta para obtener los datos de contacto de los usuarios
@user_contact_router.get ('/user_contact', tags=["Contacto"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user_contact(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener los datos de contacto de los usuarios por ID"})  
    


# ruta para consultar los datos de contacto de un usuario por el Id
@user_contact_router.get ('/user_contact/{id}', tags=["Contacto"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user_contact(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener los datos de contacto de los usuarios por ID"}) 


# ruta para actualizar  los datos de contacto de un usuario por el Id
@user_contact_router.put ('/user_contact/{id}/update', 
tags=["Contacto"], 
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se actualizó el dato de contacto del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se actualizó el dato de contacto del usuario",
                            "contactUser":"{'id': 1,'user_id': 100,'email': 'example@micorreo.com','fijo': '226656168','movil' : '939024766','created':'2023-12-01 09:00:01','updated':'2023-12-10 19:00:01','creator_user':'1','updater_user':'10'}"
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
        404: {
            "description": "No existen los datos de contacto de este usuario",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"No existen los datos de contacto de este usuario",
                            "estado":"No record found"
                        }
                    } 
                }       
            },                      
        500: {
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
def update_user_contact(userUpdaterId:int,contactUserSchema:ContactUserSchema)->dict:
    db = Session()
    result=contactUserController(db).update_contact_user(userUpdaterId,contactUserSchema)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se actualizó el registro sin problemas
        contactUser=result["contactUser"]
        return JSONResponse (status_code=201,content={"message":f"Se actualizó el contacto del usuario en el sistema","contactUser":contactUser})     
    elif (estado=="-2"):
        # no se consiguieron los datos de contacto del cliente
        return JSONResponse (status_code=404,content={"message":"No se consiguieron los datos de contacto del usuario","estado":result}) 
    else:     
        # ocurrió un error a nivel de servidor
        return JSONResponse (status_code=500,content={"message":"Ocurrió un error que no pudo ser controlado","estado":estado})     
