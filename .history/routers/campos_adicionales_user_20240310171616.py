'''
Rutas de sedes
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

#importamos el esquema de los campos adicionales del usuario
from schemas.campos_adicionales_user import CamposAdicionalesUser as CamposAdicionalesUserSchema

# importamos el controlador 
from controller.campos_adiciomales_user import CamposUserController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
campos_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear las sedes
@campos_user_router.post ('/create_campos_adicionales_user', 
tags=["Campos Adicionales Usuarios"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo una Sede en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo una Sede en el sistema",
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
def create_campos_adicionales_user(camposUser:CamposAdicionalesUserSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=CamposUserController(db).create_campos_adicionales_user(sede,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newsede=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una sede en el sistema","sede":jsonable_encoder(newsede)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una sede con este nombre, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una sede con este rut, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los campos adicionales en el sistema
@campos_user_router.get ('/list_campos_adicionales_user', 
tags=["Campos Adicionales Usuarios"],
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
def list_campos_adicionales_user()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CamposUserController(db).list_campos_adicionales_users()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar los campos adicionales de los usuarios en el sistema segun la sociedad que las agrupa
@campos_user_router.get ('/list_campos_adicionales_user_sociedad', 
tags=["Campos Adicionales Usuarios"],
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
def list_campos_adicionales_user_sociedad(idSociedad: int,)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CamposUserController(db).list_campos_adicionales_users_sociedad(idSociedad)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una sede por Id
@campos_user_router.get ('/campos_user/{id}', 
tags=["Campos Adicionales Usuarios"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Sede Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sede Encontrada",
                                    "data": "{'sociedad_id': '1','id': '1','region_id': '1','direccion': 'DIRECCION SEDE DEMO','ciudad': 'DEMO CIUDAD','updated': '2024-02-01T13:14:54','updater_user': '1','nombre': 'SEDE UNO',   'comuna_id': '1101','created': '2024-02-01T13:13:35','creator_user': '1'}",
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
            "description": "Banco no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Banco no encontrado"
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
    }   
)
def get_campos_adicionales_user(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CamposUserController(db).get_campos_adicionales_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"sede":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"sede no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"sede no encontrada"})      



# ruta para listar los datos historicos de la sedes por ID
@campos_user_router.get ('/campos_user/{id}/list_historico', 
tags=["Campos Adicionales Usuarios"],

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
def list_history_campos_adicionales_user(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CamposUserController(db).list_history_campos_adicionales_users(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para actualizar los campos adicionales por Id
@campos_user_router.put ('/campos_user/{id}/update', 
tags=["Campos Adicionales Usuarios"],
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
def update_campos_adicionales_user(camposUser:CamposAdicionalesUserSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = CamposUserController(db).update_campos_adicionales_user(user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Campos Adicioanales actualizados","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Campos Adicioanales no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        


