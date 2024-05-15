'''
Rutas de Periodos
2024-01
'''
import os
from datetime import datetime

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

#importamos el esquema de la periodo
from schemas.periodos import Periodos as PeriodosSchema

# importamos el controlador 
from controller.periodos import PeriodosController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
periodos_router = APIRouter(prefix="/V1.0")

anio_actual= datetime.now().year

# -------- Rutas Periodos ------------
# ruta para crear los periodoso
@periodos_router.post ('/create_periodo', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo una periodo en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo una periodo en el sistema",
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
def create_periodo(periodos:PeriodosSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=PeriodosController(db).create_periodo(periodos,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newperiodo=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una periodo en el sistema","periodo":jsonable_encoder(newperiodo)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una periodo con este nombre, no puede volver a crearlo","periodo":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una periodo con ese mes y el mismo año. no puede volver a crfearlo","periodo":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los periodos en el sistema
@periodos_router.get ('/list_all_periodos', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Periodo encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Periodo encontrado",
                                    "data": "{'id': '1','observaciones': '','nombre': 'Enero-2020','utm': '0','factor_actualizacion': 1026,'updated': '2024-02-01T01:00:00','updater_user': '1','anio': '2020','mes': '1','activo': '0','uf': '0','created': '2024-02-01T01:00:00','creator_user': '1'}",
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
def list_all_periodos()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = PeriodosController(db).list_all_periodos()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una periodo por Id
@periodos_router.get ('/periodo/{id}', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Periodo encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Periodo encontrado",
                                    "data": "{'id': '1','observaciones': '','nombre': 'Enero-2020','utm': '0','factor_actualizacion': 1026,'updated': '2024-02-01T01:00:00','updater_user': '1','anio': '2020','mes': '1','activo': '0','uf': '0','created': '2024-02-01T01:00:00','creator_user': '1'}",
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
            "description": "Periodo no encontrado",
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
def get_periodo(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = PeriodosController(db).get_periodo(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"periodo":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"periodo no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"periodo no encontrada"})   


# ruta para consultar detalles periodo por anio
@periodos_router.get ('/periodo/{anio}/list_details', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Periodos Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Periodos Encontrados",
                                    "data": "{'id': '1','observaciones': '','nombre': 'Enero-2020','utm': '0','factor_actualizacion': 1026,'updated': '2024-02-01T01:00:00','updater_user': '1','anio': '2020','mes': '1','activo': '0','uf': '0','created': '2024-02-01T01:00:00','creator_user': '1'}",
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
                            "message":"Periodos no encontrado"
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
def get_periodos_by_anio(anio: int = Path (ge=os.getenv("MIN_ANIO_PERIODO"),le=anio_actual)):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = PeriodosController(db).get_periodos_by_anio(anio)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"periodo":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Periodo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Periodo no encontrado"})      



# ruta para listar los datos historicos de la periodos por ID
@periodos_router.get ('/periodo/{id}/list_historico', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Periodos Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Periodos Encontrados",
                                    "data": "{'id': '1','observaciones': '','nombre': 'Enero-2020','utm': '0','factor_actualizacion': 1026,'updated': '2024-02-01T01:00:00','updater_user': '1','anio': '2020','mes': '1','activo': '0','uf': '0','created': '2024-02-01T01:00:00','creator_user': '1'}",
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
def list_history_periodo(id : int =Path(ge=1, lt=10000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = PeriodosController(db).list_history_periodos(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para actualizar una periodo por Id
@periodos_router.put ('/periodo/{id}/update', 
tags=["Periodos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Periodo actualizado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Periodo actualizado",
                                    "data": "{'id': '1','observaciones': '','nombre': 'Enero-2020','utm': '0','factor_actualizacion': 1026,'updated': '2024-02-01T01:00:00','updater_user': '1','anio': '2020','mes': '1','activo': '0','uf': '0','created': '2024-02-01T01:00:00','creator_user': '1'}",
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
def update_periodo(periodos:PeriodosSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=10000))->dict:
    db = Session()
    # buscamos el registro
    result = PeriodosController(db).update_periodo(periodos, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"periodo actualizado","periodo":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Periodo no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        

