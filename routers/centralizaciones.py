'''
Rutas de Centralizaciones
2024-03
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

#importamos el schema de datos de centralizaciones
from schemas.centralizaciones import Centralizaciones as CentralizacionesSchema


# importamos el controlador 
from controller.centralizaciones import CentralizacionesController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
centralizaciones_router = APIRouter(prefix="/V1.0")

# -------- Rutas Centralizaciones ------------
# ruta para crear las Instituciones Bancaria
@centralizaciones_router.post ('/create_centralizaciones', 
tags=["Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo  una Centralizacion en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo  una Centralizacion en el sistema",
                            "data":"{'id': '1','sociedad_id': '1','usa_centros_costos': '1','cuenta_anticipo': '','cuenta_bonos_feriado': '','cuenta_honorarios': '','cuenta_prestamos_solidarios': '','prestamo_solidario_imponible': '1',   'created': '2024-03-25T21:56:32','updated': '2024-03-25T21:56:32','creator_user': '1','updater_user': '1'}"
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
def create_centralizaciones(centralizacion:CentralizacionesSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=CentralizacionesController(db).create_centralizacion(centralizacion,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newBanco=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo  una Centralizacion en el sistema","Centralizacion":jsonable_encoder(newBanco)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una Centralizacion para esta sociedad, no puede volver a crearlo","Centralizacion":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             


# ruta para consultar una Institución Bancaria por Id
@centralizaciones_router.get ('/centralizacion/{id}', 
tags=["Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Centralizacion encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Centralizacion encontrada",
                                    "data":"{'id': '1','sociedad_id': '1','usa_centros_costos': '1','cuenta_anticipo': '','cuenta_bonos_feriado': '','cuenta_honorarios': '','cuenta_prestamos_solidarios': '','prestamo_solidario_imponible': '1',   'created': '2024-03-25T21:56:32','updated': '2024-03-25T21:56:32','creator_user': '1','updater_user': '1'}"
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
            "description": "Centralizacion no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Centralizacion no encontrado"
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
def get_centralizaciones(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CentralizacionesController(db).get_centralizacion(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Centralizacion":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Centralizacion no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Centralizacion no encontrado"})      



# ruta para listar los bancos en el sistema
@centralizaciones_router.get ('/centralizacion/{id}/list_historico', 
tags=["Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Centralizacion encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Centralizacion encontrada",
                                    "data":"{'id': '1','sociedad_id': '1','usa_centros_costos': '1','cuenta_anticipo': '','cuenta_bonos_feriado': '','cuenta_honorarios': '','cuenta_prestamos_solidarios': '','prestamo_solidario_imponible': '1',   'created': '2024-03-25T21:56:32','updated': '2024-03-25T21:56:32','creator_user': '1','updater_user': '1','fecha_registro':'2024-03-25T21:56:32','observaciones':'Creado'}"
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
def list_history_centralizacioness( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CentralizacionesController(db).list_history_centralizaciones(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 




# ruta para actualizar una centralizacion por Id
@centralizaciones_router.put ('/centralizacion/{id}/update', 
tags=["Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    {
        201: {
                "description": "Centralizacion encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Centralizacion encontrada",
                                    "data":"{'id': '1','sociedad_id': '1','usa_centros_costos': '1','cuenta_anticipo': '','cuenta_bonos_feriado': '','cuenta_honorarios': '','cuenta_prestamos_solidarios': '','prestamo_solidario_imponible': '1',   'created': '2024-03-25T21:56:32','updated': '2024-03-25T21:56:32','creator_user': '1','updater_user': '1'}"
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
def update_centralizaciones(centralizacion:CentralizacionesSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = CentralizacionesController(db).update_centralizacion( centralizacion, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Centralizacion actualizada","Centralizacion":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Centralizacion no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
