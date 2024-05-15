'''
Rutas de Datos Pago
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

#importamos el esquema de la sede
from schemas.datos_pago import DatosPago as DatosPagoSchema

# importamos el controlador 
from controller.datos_pago import DatosPagoController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
datos_pago_router = APIRouter(prefix="/V1.0")

# -------- Rutas Datos de Pago ------------
# ruta para crear las Datos de Pago
@datos_pago_router.post ('/create_datos_pago', 
tags=["Datos Pago"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Dato de Pago sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Dato de Pago en el sistema",
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
        521: {
            "description": "Este usuario ya tiene Datos de Pago no puede volver a crearlo",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de pago Encontrados",
                                    "data": "{'id': '1','user_id': '1','medio': '1','tipo_cuenta': '1','banco_id': '1','created': '2024-03-03T20:31:16','updated': '2024-03-03T20:31:16','creator_user': '1','updater_user': '1'}",
                                }
                        } 
                    
                }       
            },                                
    }                      
)
def create_datos_pago(datosPago:DatosPagoSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=DatosPagoController(db).create_datos_pago(datosPago,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1"):
        # se inserto el registro sin problemas
        newDatoLaboral=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Dato de Pago en el sistema","Dato de Pago":jsonable_encoder(newDatoLaboral)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        datoLaboral=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario ya tiene Datos de Pago no puede volver a crearlo","Dato de Pago Existente":jsonable_encoder(datoLaboral)})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los datos de pago en el sistema
@datos_pago_router.get ('/list_datos_pago', 
tags=["Datos Pago"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos de Pago Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Pago Encontrados",
                                    "data": "{'id': '1','user_id': '1','medio': '1','tipo_cuenta': '1','banco_id': '1','created': '2024-03-03T20:31:16','updated': '2024-03-03T20:31:16','creator_user': '1','updater_user': '1'}",
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
def list_datos_pago()->dict:
    db = Session()
    # almacenamos el listado de datos de pago en un resulset
    result = DatosPagoController(db).list_datos_pago()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 

       


# ruta para listar los datos de pago  en el sistema segun el user
@datos_pago_router.get ('/get_datos_pago_user', 
tags=["Datos Pago"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos de Pago Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Pago Encontrados",
                                    "data": "{'id': '1','user_id': '1','medio': '1','tipo_cuenta': '1','banco_id': '1','created': '2024-03-03T20:31:16','updated': '2024-03-03T20:31:16','creator_user': '1','updater_user': '1'}",
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
def list_datos_pago_user(iduser: int)->dict:
    db = Session()
    # almacenamos el listado de datos de pago en un resulset
    result = DatosPagoController(db).get_datos_pago_userid(iduser)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        



# ruta para consultar dato de pago por Id
@datos_pago_router.get ('/datos_pago/{id}', 
tags=["Datos Pago"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos de Pago Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Pago Encontrados",
                                    "data": "{'id': '1','user_id': '1','medio': '1','tipo_cuenta': '1','banco_id': '1','created': '2024-03-03T20:31:16','updated': '2024-03-03T20:31:16','creator_user': '1','updater_user': '1'}",
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
            "description": "Dato de Pago no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Dato de Pago no encontrado"
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
def get_datos_pago(id: int):
    db = Session()
    # almacenamos el listado de datos de pago en un resulset
    result = DatosPagoController(db).get_datos_pago(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Dato de Pago encontrado":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Dato de Pago no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Dato de Pago no encontrado"})      



# ruta para listar los datos historicos de un dato de pago por ID
@datos_pago_router.get ('/datos_pago/{id}/list_historico', 
tags=["Datos Pago"],

responses=
    { 
        200: {
                "description": "Datos de Pago Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Pago Encontrados",
                                    "data": "{'id': '1','user_id': '1','medio': '1','tipo_cuenta': '1','banco_id': '1','created': '2024-03-03T20:31:16','updated': '2024-03-03T20:31:16','creator_user': '1','updater_user': '1'}",
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
            "description": "No hay registros que mostrar",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"No hay registros que mostrar"
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
def list_history_datos_pago(id)->dict:
    db = Session()
    # almacenamos el listado de datos de pago en un resulset
    result = DatosPagoController(db).list_history_datos_pago(id)

    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Datos de Pago":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})     
    
    
    return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})        



# ruta para actualizar  un dato de porago por Id
@datos_pago_router.put ('/datos_pago/{id}/update', 
tags=["Datos Pago"],
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
        404: {
            "description": "Dalo de Pago no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Dalo de Pago no encontrado"
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
def update_datos_pago(datosPago:DatosPagoSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = DatosPagoController(db).update_datos_pago(datosPago, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Dato de Pago actualizado","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Dato de Pago no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        


