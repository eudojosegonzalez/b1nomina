
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
from schemas.contact_user import ContactUser as ContactoSchema


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
def create_user_contact()->dict:
    db = Session()
    result=contactUserController(db).create_contact_user(ContactoSchema)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newContactUserId=result["newContactUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el contacto del usuario en el sistema","newUserId":newContactUserId})     
    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})      
    
       

# ruta para listar los datos de contacto de los usuarios
@user_contact_router.get ('/user_contact', tags=["Contacto"],status_code=200, dependencies=[Depends(JWTBearer())])
def list_user_contact():
    return JSONResponse (status_code=201,content={"message":"Se obtuvo un listadolos datos de contacto de los usuarios"})  

# ruta para consultar los datos de contacto de un usuario por el Id
@user_contact_router.get ('/user_contact/{id}', tags=["Contacto"],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user_contact(id: int):
    return JSONResponse (status_code=200,content={"message":"Obtener los datos de contacto de los usuarios por ID"})  

# ruta para actualizar  los datos de contacto de un usuario por el Id
@user_contact_router.put ('/user_contact/{id}/update', tags=["Contacto"],status_code=200, dependencies=[Depends(JWTBearer())])
def update_user_contact(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar los datos de contacto de los usuarios por ID"})      
