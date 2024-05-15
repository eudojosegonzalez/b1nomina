'''
Rutas de AFC de usuario
Created: 2024-03
'''

import os

#importamos la libreria para cargar los archivos de entorno
import dotenv


#importamos la libreria FASTAPI
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
from controller.usuarios_afc import UsuariosAFCController



#importamos el esquema de datos para utilizarlo como referencia de datos a la hora de capturar data
from schemas.usuarios_afc import UsuariosAFC as UsuariosAFCSchema


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
usuarios_afc_router = APIRouter(prefix="/V1.0")

# -------- Rutas Ubicación Usuario  ------------
# ruta para crear los datos de contacto de un usuario
@usuarios_afc_router.post ('/create_user_afc', 
tags=["AFC Usuarios"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo el registro AFC del Usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el registro AFC del Usuario",
                            "newUserAFCId":"1"
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
        521: {
            "description": "Ya existen los datos de ubicación de este usuario, no puede volver a crearlos",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Ya existen los datos de ubicacion de este usuario, no puede volver a crearlos",
                            "estado":"Record found"
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
def create_user_afc(usuarioAfC:UsuariosAFCSchema, userCreatorId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=UsuariosAFCController(db).create_usuario_afc(userCreatorId,usuarioAfC)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUsuarioAFC=result["UsuarioAFC"]
        return JSONResponse (status_code=201,content={"message":"Se creo el regfistro AFC del usuario en el sistema","newUsuarioAFC":jsonable_encoder(newUsuarioAFC)})     
    elif (estado=="-2"):
        usuarioAFC=result["usuarioAFC"]
        return JSONResponse (status_code=521,content={"message":"Ya existen los datos de AFC de este usuario, no puede volver a crearlos","usuarioAFC":jsonable_encoder(usuarioAFC)})    
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})              


# ruta para consultar los datos de ubicacion de un usuario por el Id
@usuarios_afc_router.get ('/user_afc/{id}',
tags=["AFC Usuarios"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se consiguieron los datos de AFC del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se consiguieron los datos de AFC del usuario",
                            "ubicacionUser":"{'id': 1,'user_id': 100,'email': 'example@micorreo.com','fijo': '226656168','movil' : '939024766','created':'2023-12-01 09:00:01','updated':'2023-12-10 19:00:01','creator_user':'1','updater_user':'10'}"
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
def get_user_afc(id: int  = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=UsuariosAFCController(db).get_usuario_afc(id)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se consiguieron los datos de AFC del usuario
        UsuarioAFC=result["UsuarioAFC"]
        return JSONResponse (status_code=201,content={"message":"Se consiguieron los datos de AFC del usuario en el sistema","UsuarioAFC":UsuarioAFC})     
    elif (estado=="-2"):
        # no se consiguieron los datos de contacto del cliente
        return JSONResponse (status_code=404,content={"message":"No se consiguieron los datos de AFC del usuario","estado":result}) 
    else:     
        # ocurrió un error a nivel de servidor
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":estado}) 


# ruta para consultar los datos historicos de contacto de un usuario por el Id
@usuarios_afc_router.get ('/user_afc/{id}/list_historico',
tags=["AFC Usuarios"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se consiguieron los datos de AFC del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se consiguieron los datos de AFC del usuario",
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
            "description": "No existen los datos de AFC de este usuario",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"No existen los datos de AFC de este usuario",
                            "estado":"No record found"
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
def list_history_user_afc(id: int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=UsuariosAFCController(db).list_history_usuario_afc(id)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se consiguieron los datos históricos de ubicacion del usuario
        data=result["listHistoryUsarioAFC"]
        return JSONResponse (status_code=201,content=jsonable_encoder(data))     
    elif (estado=="-2"):
        # no se consiguieron los datos de contacto del cliente
        return JSONResponse (status_code=404,content={"message":"No se consiguieron los datos historicos de AFC del usuario","estado":result}) 
    else:     
        # ocurrió un error a nivel de servidor
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":estado}) 




# ruta para actualizar  los datos de contacto de un usuario por el Id
@usuarios_afc_router.put ('/user_afc/{id}/update', 
tags=["AFC Usuarios"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se actualizó el dato de ubicacion del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se actualizó el dato de ubicacion del usuario",
                            "ubicacionUser":"{'id': 1,'user_id': 100,'email': 'example@micorreo.com','fijo': '226656168','movil' : '939024766','created':'2023-12-01 09:00:01','updated':'2023-12-10 19:00:01','creator_user':'1','updater_user':'10'}"
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
            "description": "No existen los datos de ubicación de este usuario",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"No existen los datos de ubicación de este usuario",
                            "estado":"No record found"
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
def update_user_afc(usuarioAfC:UsuariosAFCSchema,userUpdaterId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")) , id : int= Path (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=UsuariosAFCController(db).update_usuario_afc(userUpdaterId, usuarioAfC, id)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se actualizó el registro sin problemas
        UsuarioAFC=result["UsuarioAFC"]
        return JSONResponse (status_code=201,content={"message":f"Se actualizó el registro AFC del usuario en el sistema","UsuarioAFC":jsonable_encoder(UsuarioAFC)})     
    elif (estado=="-2"):
        # no se consiguieron los datos de contacto del cliente
        return JSONResponse (status_code=404,content={"message":"No se consiguieron los datos de AFC del usuario","estado":result}) 
    else:     
        # ocurrió un error a nivel de servidor
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":estado})     
