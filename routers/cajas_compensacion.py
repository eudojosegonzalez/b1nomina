'''
Rutas de Cajas de Compensacion
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
from schemas.cajas_compensacion import CajasCompensacion as CajasCompensacionSchema

# importamos el controlador 
from controller.caja_compensacion import CajasCompensacionController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
cajas_compensacion_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear las Cajas de compensacion
@cajas_compensacion_router .post ('/create_cajas_compensacion', 
tags=["Cajas Compensacion"],
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
def create_cajas_compensacion(cajasCompensacion:CajasCompensacionSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=CajasCompensacionController(db).create_cajas_compensacion(cajasCompensacion,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newsede=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una Caja de Compensacion el sistema","Caja Compensacion":jsonable_encoder(newsede)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una Caja de Compensacion con ese nombre, no puede volver a crearla","Caja Compensacion":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las Cajas de compensacion en el sistema
@cajas_compensacion_router .get ('/list_cajas_compensacion', 
tags=["Cajas Compensacion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Caja de Compensacion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Caja de Compensacion Encontrada",
                                    "data": "{ 'id': '1','nombre': 'Sin CCAF', 'codigo_externo': '00','cuenta_contable': '21050003',   'codigo_direccion_trabajo': '0',  'created': '1990-01-01T00:00:00', 'updated': '1990-01-01T00:00:00', 'creator_user': '1','updater_user': '1'}",
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
def list_cajas_compensacion()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CajasCompensacionController(db).list_cajas_compensacion()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 



# ruta para consultar una caja de compensacion por Id
@cajas_compensacion_router .get ('/cajas_compensacion/{id}', 
tags=["Cajas Compensacion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Caja de Compensacion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Caja de Compensacion Encontrada",
                                    "data": "{ 'id': '1','nombre': 'Sin CCAF', 'codigo_externo': '00','cuenta_contable': '21050003',   'codigo_direccion_trabajo': '0',  'created': '1990-01-01T00:00:00', 'updated': '1990-01-01T00:00:00', 'creator_user': '1','updater_user': '1'}",
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
def get_cajas_compensacion(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CajasCompensacionController(db).get_cajas_compensacion(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Tipo de Prestamo":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Tipo de Prestamo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Tipo de Prestamo no encontrado"})      



# ruta para listar los datos historicos de la sedes por ID
@cajas_compensacion_router .get ('/cajas_compensacion/{id}/list_historico', 
tags=["Cajas Compensacion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Caja de Compensacion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Caja de Compensacion Encontrada",
                                    "data": "{ 'id': '1','nombre': 'Sin CCAF', 'codigo_externo': '00','cuenta_contable': '21050003',   'codigo_direccion_trabajo': '0',  'created': '1990-01-01T00:00:00', 'updated': '1990-01-01T00:00:00', 'creator_user': '1','updater_user': '1'}",
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
def list_history_cajas_compensacion(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CajasCompensacionController(db).list_history_cajas_compensacion(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sede por nombre o rut
@cajas_compensacion_router .get ('/search_cajas_compensacion', 
tags=["Cajas Compensacion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Caja de Compensacion Encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Caja de Compensacion Encontrada",
                                    "data": "{ 'id': '1','nombre': 'Sin CCAF', 'codigo_externo': '00','cuenta_contable': '21050003',   'codigo_direccion_trabajo': '0',  'created': '1990-01-01T00:00:00', 'updated': '1990-01-01T00:00:00', 'creator_user': '1','updater_user': '1'}",
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
def search_cajas_compensacion(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CajasCompensacionController(db).search_cajas_compensacion(finding)
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
@cajas_compensacion_router .put ('/cajas_compensacion/{id}/update', 
tags=["Cajas Compensacion"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Caja de Compensacion Actualizada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Caja de Compensacion Actualizada",
                                    "data": "{ 'id': '1','nombre': 'Sin CCAF', 'codigo_externo': '00','cuenta_contable': '21050003',   'codigo_direccion_trabajo': '0',  'created': '1990-01-01T00:00:00', 'updated': '1990-01-01T00:00:00', 'creator_user': '1','updater_user': '1'}",
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
def update_cajas_compensacion(cajasCompensacion:CajasCompensacionSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = CajasCompensacionController(db).update_cajas_compensacion(cajasCompensacion, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Caja de Compensación actualizada","Caja de Compensacion":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Caja de Compensación actualizada no encontrada"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        

