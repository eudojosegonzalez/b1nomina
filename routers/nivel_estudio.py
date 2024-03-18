'''
Rutas de Nivel de Estudio
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

#importamos el esquema de Niveles de Estudio
from schemas.nivel_estudio import NivelEstudio as NivelEstudioSchema

# importamos el controlador 
from controller.nivel_estudio import NivelEstudioController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
nivel_estudio_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear las sedes
@nivel_estudio_router.post ('/create_nivel_estudio', 
tags=["Nivel Estudio"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Nivel de Estudo en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Nivel de Estudo en el sistema",
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
def create_nivel_estudio(nivelEstudio:NivelEstudioSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=NivelEstudioController(db).create_nivel_estudio(nivelEstudio,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newsede=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Nivel de Estudo en el sistema","sede":jsonable_encoder(newsede)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe un Nivel de Estudo con este nombre, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe un Nivel de Estudo con este rut, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las sedes en el sistema
@nivel_estudio_router.get ('/list_nivel_estudio', 
tags=["Nivel Estudio"],
#dependencies=[Depends(JWTBearer())],
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
def list_nivel_estudio()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = NivelEstudioController(db).list_nivel_estudio()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 





# ruta para consultar un Nivel de Estudo por Id
@nivel_estudio_router.get ('/nivel_estudio/{id}', 
tags=["Nivel Estudio"],
#dependencies=[Depends(JWTBearer())],
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
def get_nivel_estudio(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = NivelEstudioController(db).get_nivel_estudio(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"sede":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"sede no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"sede no encontrada"})      



# ruta para listar los datos historicos de la sedes por ID
@nivel_estudio_router.get ('/nivel_estudio/{id}/list_historico', 
tags=["Nivel Estudio"],

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
def list_history_nivel_estudio( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = NivelEstudioController(db).list_history_nivel_estudio(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar un Nivel de Estudo por nombre o rut
@nivel_estudio_router.get ('/search_nivel_estudio', 
tags=["Nivel Estudio"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Sede encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sede encontrada",
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
def search_nivel_estudio(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = NivelEstudioController(db).search_nivel_estudio(finding)
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


# ruta para actualizar un Nivel de Estudo por Id
@nivel_estudio_router.put ('/nivel_estudio/{id}/update', 
tags=["Nivel Estudio"],
#dependencies=[Depends(JWTBearer())],
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
def update_nivel_estudio(nivelEstudio:NivelEstudioSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = NivelEstudioController(db).update_nivel_estudio(nivelEstudio, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"sede actualizada","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Sede no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        


