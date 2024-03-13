'''
Rutas de Tramos de Asignacion Familiar
2024-02
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

#importamos el esquema de Tramos de Impuesto Único
from schemas.tramos_asignacion_familiar import TramosAsignacionFamiliar as TramosAsignacionFamiliarSchema

# importamos el controlador 
from controller.tramos_asignacion_familiar import TramoAsignacionFamiliarController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
tramos_asignacion_familiar_router = APIRouter(prefix="/V1.0")

# -------- Rutas Tramo Asignacion Familiar ------------
# ruta para crear las Tramo Asignacion Familiar
@tramos_asignacion_familiar_router.post ('/create_tramo_asignacion_familiar', 
tags=["Tramos Asignacion Familiar"],
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
def create_tramo_asignacion_familiar(tramosAsignacionFamiliar:TramosAsignacionFamiliarSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=TramoAsignacionFamiliarController(db).create_tramo_asignacion_familiar(tramosAsignacionFamiliar,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newTramoAsignacionFamiliar=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Tramo de Impuesto Único sistema","sede":jsonable_encoder(newTramoAsignacionFamiliar)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe un Tramo de Asignación este nombre, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las sedes en el sistema
@tramos_asignacion_familiar_router.get ('/list_tramo_asignacion_familiar', 
tags=["Tramos Asignacion Familiar"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo de asignación Familiar encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo de asignación Familiar encontrado",
                                    "data": "{'id': '1', 'tramo': 'A', 'desde': '0','hasta': 315841,'valor_carga': '12364','created': '2024-02-27T15:00:00','updated': '2024-02-27T15:00:00', 'creator_user': '1', 'updater_user': '1'}",
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
def list_tramo_asignacion_familiar()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramoAsignacionFamiliarController(db).list_tramo_asignacion_familiar()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una sede por Id
@tramos_asignacion_familiar_router.get ('/tramo_asignacion_fimiliar/{id}', 
tags=["Tramos Asignacion Familiar"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo de asignación Familiar encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo de asignación Familiar encontrado",
                                    "data": "{'id': '1', 'tramo': 'A', 'desde': '0','hasta': 315841,'valor_carga': '12364','created': '2024-02-27T15:00:00','updated': '2024-02-27T15:00:00', 'creator_user': '1', 'updater_user': '1'}",
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
def get_tramo_asignacion_familiar(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramoAsignacionFamiliarController(db).get_tramo_asignacion_familiar(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"sede":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Tramo Impuesto Único no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Tramo Impuesto Único  no encontrada"})      



# ruta para listar los datos historicos de la sedes por ID
@tramos_asignacion_familiar_router.get ('/tramo_asignacion_fimiliar/{id}/list_historico', 
tags=["Tramos Asignacion Familiar"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo de asignación Familiar encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo de asignación Familiar encontrado",
                                    "data": "{'id': '1', 'tramo': 'A', 'desde': '0','hasta': 315841,'valor_carga': '12364','created': '2024-02-27T15:00:00','updated': '2024-02-27T15:00:00', 'creator_user': '1', 'updater_user': '1'}",
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
def list_history_tramo_asignacion_familiar( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramoAsignacionFamiliarController(db).list_history_tramo_asignacion_familiar(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sede por nombre o rut
@tramos_asignacion_familiar_router.get ('/search_tramo_asignacion_familiar', 
tags=["Tramos Asignacion Familiar"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo de asignación Familiar encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo de asignación Familiar encontrado",
                                    "data": "{'id': '1', 'tramo': 'A', 'desde': '0','hasta': 315841,'valor_carga': '12364','created': '2024-02-27T15:00:00','updated': '2024-02-27T15:00:00', 'creator_user': '1', 'updater_user': '1'}",
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
            "description": "La búsqueda no arrojó resultados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"La búsqueda no arrojó resultados"
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
def search_tramo_asignacion_familiar(finding : str = Query (min_length=1, max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramoAsignacionFamiliarController(db).search_tramo_asignacion_familiar(finding)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"La búsqueda no arrojó resultados"})    
        else:
            return JSONResponse(status_code=520,content={"message":"System Error","error":result})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})


# ruta para actualizar una sede por Id
@tramos_asignacion_familiar_router.put ('/tramo_asignacion_fimiliar/{id}/update', 
tags=["Tramos Asignacion Familiar"],
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
def update_tramo_asignacion_familiar(tramosAsignacionFamiliar:TramosAsignacionFamiliarSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = TramoAsignacionFamiliarController(db).update_tramo_asignacion_familiar(tramosAsignacionFamiliar, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Tramo de Impuesto Único actualizada","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Tramo de Impuesto Único no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        

