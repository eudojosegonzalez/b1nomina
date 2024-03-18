'''
Rutas de Tramos de Impuesto Único
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
from schemas.tramos_impuesto_unico import TramosImpuestoUnico as TramosImpuestoUnicoSchema

# importamos el controlador 
from controller.tramos_impuesto_unico import TramosImpuestoUnicoController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
tramos_impuesto_unico_router = APIRouter(prefix="/V1.0")

# -------- Rutas Tramos Impuesto Unico-----------
# ruta para crear las Tramos Impuesto Unico
@tramos_impuesto_unico_router.post ('/create_tramo_impuesto_unico', 
tags=["Tramos Impuesto Unico"],
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
def create_tramo_impuesto_unico(tramosImpuestoUnico:TramosImpuestoUnicoSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=TramosImpuestoUnicoController(db).create_tramo_impuesto_unico(tramosImpuestoUnico,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newTramoImpuestoUnico=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Tramo de Impuesto Único sistema","sede":jsonable_encoder(newTramoImpuestoUnico)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una sede con este nombre, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una sede con este rut, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las sedes en el sistema
@tramos_impuesto_unico_router.get ('/list_tramo_impuesto_unico', 
tags=["Tramos Impuesto Unico"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo Impuesto Único encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo Impuesto Único encontrado",
                                    "data": "{ 'id': '1','tramo':'Tramo 1','desde': '0','hasta': '13.5','factor':0,'rebaja':'0','created':'2024-02-26T10:00:00','updated': '2024-02-26T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_tramo_impuesto_unico()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramosImpuestoUnicoController(db).list_tramo_impuesto_unico()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una sede por Id
@tramos_impuesto_unico_router.get ('/tramo_impuesto_unico/{id}', 
tags=["Tramos Impuesto Unico"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo Impuesto Único encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo Impuesto Único encontrado",
                                    "data": "{ 'id': '1','tramo':'Tramo 1','desde': '0','hasta': '13.5','factor':0,'rebaja':'0','created':'2024-02-26T10:00:00','updated': '2024-02-26T10:00:00','creator_user': '1','updater_user': '1'}",
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
def get_tramo_impuesto_unico(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramosImpuestoUnicoController(db).get_tramo_impuesto_unico(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"sede":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Tramo Impuesto Único no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Tramo Impuesto Único  no encontrada"})      



# ruta para listar los datos historicos de la sedes por ID
@tramos_impuesto_unico_router.get ('/tramo_impuesto_unico/{id}/list_historico', 
tags=["Tramos Impuesto Unico"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo Impuesto Único encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo Impuesto Único encontrado",
                                    "data": "{ 'id': '1','tramo':'Tramo 1','desde': '0','hasta': '13.5','factor':0,'rebaja':'0','created':'2024-02-26T10:00:00','updated': '2024-02-26T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_history_tramo_impuesto_unico( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramosImpuestoUnicoController(db).list_history_tramo_impuesto_unico(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sede por nombre o rut
@tramos_impuesto_unico_router.get ('/search_tramo_impuesto_unico', 
tags=["Tramos Impuesto Unico"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tramo Impuesto Único encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tramo Impuesto Único encontrado",
                                    "data": "{ 'id': '1','tramo':'Tramo 1','desde': '0','hasta': '13.5','factor':0,'rebaja':'0','created':'2024-02-26T10:00:00','updated': '2024-02-26T10:00:00','creator_user': '1','updater_user': '1'}",
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
def search_tramo_impuesto_unico(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TramosImpuestoUnicoController(db).search_tramo_impuesto_unico(finding)
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
@tramos_impuesto_unico_router.put ('/tramo_impuesto_unico/{id}/update', 
tags=["Tramos Impuesto Unico"],
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
def update_tramo_impuesto_unico(tramosImpuestoUnico:TramosImpuestoUnicoSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = TramosImpuestoUnicoController(db).update_tramo_impuesto_unico(tramosImpuestoUnico, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Tramo de Impuesto Único actualizada","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Tramo de Impuesto Único no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        

