'''
Rutas de Categorias de Configuracion
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
from schemas.categorias_configuracion import CategoriasConfiguracion as CategoriasConfiguracionSchema

# importamos el controlador 
from controller.categorias_configuracion import CategoriasConfiguracionController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
categorias_configuracion_router = APIRouter(prefix="/V1.0")

# -------- Rutas categorias_configuracions ------------
# ruta para crear las categorias_configuracions
@categorias_configuracion_router.post ('/create_categorias_configuracion', 
tags=["Categorias Configuracion"],
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
def create_categorias_configuracion(categorias_configuracion:CategoriasConfiguracionSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=CategoriasConfiguracionController(db).create_categoria_configuracion(categorias_configuracion,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newcategorias_configuracion=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una categorias_configuracion en el sistema","categorias_configuracion":jsonable_encoder(newcategorias_configuracion)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una categorias_configuracion con este nombre, no puede volver a crearla","categorias_configuracion":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una categorias_configuracion con este rut, no puede volver a crearla","categorias_configuracion":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las categorias_configuracions en el sistema
@categorias_configuracion_router.get ('/list_categorias_configuracion', 
tags=["Categorias Configuracion"],
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
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'CONFIGURACIONES BASICAS','activo': 'true','created': '2024-02-13T10:00:00','updated': '2024-02-13T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_categorias_configuracion()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CategoriasConfiguracionController(db).list_categorias_configuracion()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar las categorias_configuracions en el sistema segun la sociedad que las agrupa
@categorias_configuracion_router.get ('/list_categorias_configuracion_sociedad', 
tags=["Categorias Configuracion"],
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
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'CONFIGURACIONES BASICAS','activo': 'true','created': '2024-02-13T10:00:00','updated': '2024-02-13T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_categorias_configuracion_sociedad(idSociedad: int, )->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CategoriasConfiguracionController(db).list_categorias_configuracion_sociedad(idSociedad)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una categorias_configuracion por Id
@categorias_configuracion_router.get ('/categorias_configuracion/{id}', 
tags=["Categorias Configuracion"],
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
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'CONFIGURACIONES BASICAS','activo': 'true','created': '2024-02-13T10:00:00','updated': '2024-02-13T10:00:00','creator_user': '1','updater_user': '1'}",
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
def get_categorias_configuracion(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CategoriasConfiguracionController(db).get_categoria_configuracion(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"categorias_configuracion":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"categorias_configuracion no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"categorias_configuracion no encontrada"})      



# ruta para listar los datos historicos de la categorias_configuracions por ID
@categorias_configuracion_router.get ('/categorias_configuracion/{id}/list_historico', 
tags=["Categorias Configuracion"],

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
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'CONFIGURACIONES BASICAS','activo': 'true','created': '2024-02-13T10:00:00','updated': '2024-02-13T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_history_categorias_configuracion( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CategoriasConfiguracionController(db).list_history_categoria_configuracion(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para actualizar una categorias_configuracion por Id
@categorias_configuracion_router.put ('/categorias_configuracion/{id}/update', 
tags=["Categorias Configuracion"],
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
def update_categorias_configuracion(categorias_configuracion:CategoriasConfiguracionSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = CategoriasConfiguracionController(db).update_categoria_configuracion(categorias_configuracion, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"categorias_configuracion actualizada","categorias_configuracion":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"categorias_configuracion no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
