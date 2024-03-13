'''
Rutas de Tipos de Prestamos
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

#importamos el esquema de la sede
from schemas.tipos_prestamos import TiposPrestamos as TiposPrestamosSchema

# importamos el controlador 
from controller.tipos_prestamos import TiposPrestamosController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
tipos_prestamos_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear los tipos de prestamos
@tipos_prestamos_router .post ('/create_tipos_prestamos', 
tags=["Tipos Prestamos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo Tipo de Prestamo en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo Tipo de Prestamo en el sistema",
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
def create_tipos_prestamos(tiposPrestamos:TiposPrestamosSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=TiposPrestamosController(db).create_tipos_prestamos(tiposPrestamos,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newsede=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Tipo de Prestamo en el sistema","sede":jsonable_encoder(newsede)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe un Tipo de Prestamo con ese nombre, no puede volver a crearla","sede":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los tipos de prestamos en el sistema
@tipos_prestamos_router .get ('/list_tipos_prestamos', 
tags=["Tipos Prestamos"],
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
def list_tipos_prestamos()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TiposPrestamosController(db).list_tipos_prestamos()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar los tipos de prestamos en el sistema segun la sociedad que las agrupa
@tipos_prestamos_router .get ('/list_tipos_prestamos_sociedad', 
tags=["Tipos Prestamos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tipo de Prestamo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tipo de Prestamo Encontrado",
                                    "data": "{'id': '2','sociedad_id': '1','descripcion': 'CCAF','CCAF': '1','cuenta': '21050003','caja_compensacion_id': 'null','created': '2024-02-21T10:00:00','updated': '2024-02-21T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_tipos_prestamos_sociedad(idSociedad: int)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TiposPrestamosController(db).list_tipos_prestamos_sociedad(idSociedad)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una sede por Id
@tipos_prestamos_router .get ('/tipos_prestamos/{id}', 
tags=["Tipos Prestamos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tipo de Prestamo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tipo de Prestamo Encontrado",
                                    "data": "{'id': '2','sociedad_id': '1','descripcion': 'CCAF','CCAF': '1','cuenta': '21050003','caja_compensacion_id': 'null','created': '2024-02-21T10:00:00','updated': '2024-02-21T10:00:00','creator_user': '1','updater_user': '1'}",
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
            "description": "Tipo de Prestamo no encontrado",
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
def get_tipos_prestamos(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TiposPrestamosController(db).get_tipos_prestamos(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Tipo de Prestamo":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Tipo de Prestamo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Tipo de Prestamo no encontrado"})      



# ruta para listar los datos historicos de la sedes por ID
@tipos_prestamos_router .get ('/tipos_prestamos/{id}/list_historico', 
tags=["Tipos Prestamos"],
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
def list_history_tipos_prestamos(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TiposPrestamosController(db).list_history_tipos_prestamos(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sede por nombre o rut
@tipos_prestamos_router .get ('/search_tipos_prestamos', 
tags=["Tipos Prestamos"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tipo de Prestamo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tipo de Prestamo Encontrado",
                                    "data": "{'id': '2','sociedad_id': '1','descripcion': 'CCAF','CCAF': '1','cuenta': '21050003','caja_compensacion_id': 'null','created': '2024-02-21T10:00:00','updated': '2024-02-21T10:00:00','creator_user': '1','updater_user': '1'}",
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
def search_tipos_prestamos(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = TiposPrestamosController(db).search_tipos_prestamos(finding)
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
@tipos_prestamos_router .put ('/tipos_prestamos/{id}/update', 
tags=["Tipos Prestamos"],
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
def update_tipos_prestamos(tiposPrestamos:TiposPrestamosSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = TiposPrestamosController(db).update_tipos_prestamos(tiposPrestamos, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Tipo de Prestamo actualizado","Tipo de Prestamo":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"ipo de Prestamo no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        

