'''
Rutas de Configuracion
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

#importamos el esquema de las categorias de Configuracion
from schemas.configuracion import Configuraciones as ConfiguracionesSchema

# importamos el controlador 
from controller.configuracion import ConfiguracionController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
configuracion_router = APIRouter(prefix="/V1.0")

# -------- Rutas categorias_configuracions ------------
# ruta para crear las categorias_configuracions
@configuracion_router.post ('/create_configuracion', 
tags=["Configuracion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo una categorias_configuracion en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo una categorias_configuracion en el sistema",
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
def create_configuracion(configuracion:ConfiguracionesSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=ConfiguracionController(db).create_configuracion(configuracion,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newConfiguracion=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una Cconfiguracion en el sistema","Configuracion":jsonable_encoder(newConfiguracion)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una Configuracion con este nombre, no puede volver a crearla","Configuracion":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las categorias_configuracions en el sistema
@configuracion_router.get ('/list_configuracion', 
tags=["Configuracion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "categorias_configuracion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"categorias_configuracion Encontrada",
                                    "data": "{'id': '1','nombre': 'Sueldo Minimo ($)','detalle': '','ocultar': '0','orden': '1','updated': '2024-02-19T10:00:00','updater_user': '1','valor': '445000','sociedad_id': '1',  'categoria_id': '1','cuenta': '','tipo_validacion': 'Numérico','created': '2024-02-19T10:00:00','creator_user': '1'}",
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
def list_configuracion()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ConfiguracionController(db).list_configuracion()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar las categorias_configuracions en el sistema segun la sociedad que las agrupa
@configuracion_router.get ('/list_configuracion_sociedad', 
tags=["Configuracion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "categorias_configuracion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"categorias_configuracion Encontrada",
                                    "data": "{'id': '1','nombre': 'Sueldo Minimo ($)','detalle': '','ocultar': '0','orden': '1','updated': '2024-02-19T10:00:00','updater_user': '1','valor': '445000','sociedad_id': '1',  'categoria_id': '1','cuenta': '','tipo_validacion': 'Numérico','created': '2024-02-19T10:00:00','creator_user': '1'}",
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
def list_configuracion_sociedad(idSociedad: int, )->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ConfiguracionController(db).list_configuracion_sociedad(idSociedad)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una categorias_configuracion por Id
@configuracion_router.get ('/configuracion/{id}', 
tags=["Configuracion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Cconfiguracion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"categorias_configuracion Encontrada",
                                    "data": "{'id': '1','nombre': 'Sueldo Minimo ($)','detalle': '','ocultar': '0','orden': '1','updated': '2024-02-19T10:00:00','updater_user': '1','valor': '445000','sociedad_id': '1',  'categoria_id': '1','cuenta': '','tipo_validacion': 'Numérico','created': '2024-02-19T10:00:00','creator_user': '1'}",
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
def get_configuracion(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ConfiguracionController(db).get_configuracion(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Configuracion":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Configuracion no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Configuracion no encontrada"})      



# ruta para listar los datos historicos de la categorias_configuracions por ID
@configuracion_router.get ('/configuracion/{id}/list_historico', 
tags=["Configuracion"],

responses=
    { 
        200: {
                "description": "Historico de Categorias de Configuracion encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Historico de Categorias de Configuracion encontrada",
                                    "data": "{'id': '1','nombre': 'Sueldo Minimo ($)','detalle': '','ocultar': '0','orden': '1','updated': '2024-02-19T10:00:00','updater_user': '1','valor': '445000','sociedad_id': '1',  'categoria_id': '1','cuenta': '','tipo_validacion': 'Numérico','created': '2024-02-19T10:00:00','creator_user': '1'}",
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
def list_history_configuracion( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ConfiguracionController(db).list_history_configuracion(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para actualizar una categorias_configuracion por Id
@configuracion_router.put ('/configuracion/{id}/update', 
tags=["Configuracion"],
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
def update_configuracion(configuracion:ConfiguracionesSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = ConfiguracionController(db).update_configuracion(configuracion, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"configuracion actualizada","categorias_configuracion":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"configuracion no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
