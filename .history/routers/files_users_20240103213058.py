'''
Rutas de Contacto de usuario
Created: 2023-12
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv


from fastapi import File, UploadFile,  Request

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
from controller.files_users import FilesUserController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
files_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Archivos Usuario ------------

# Funcion para subir archivos al profile de un usuario
@files_user_router.post ('/user/{id}/upload_file_users',
tags=['Archivos de Usuarios'],
#dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un archivo de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un archivo de usuarios al sistema",
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
          521: {
            "description": "Tipo de archivo no permitido",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Tipo de archivo no permitido",
                            'Archivos Permitidos': ['png','jpg','jpeg','gif','pdf']
                        }
                    } 
                }       
            }, 
          522: {
            "description": "El archivo es demasiado grande",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El archivo es demasiado grande",
                            "estado":"El archivo es demasiado grande, tamaño máximo permitido 20Mb"
                        }
                    } 
                }       
            },                                             
    })
async def file_upload_user(creatorUserId : int = Query (ge=1, lt=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, lt=os.getenv("MAX_ID_USERS")),file : UploadFile=File())->dict:
    db = Session()
    result=FilesUserController(db).upload_file_user(creatorUserId,id,file)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newFileUserId=result["newFileUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el archivo del usuario en el sistema","newfileUserId":newFileUserId})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})    
    elif  (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})        
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})

