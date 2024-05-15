'''
Rutas de Bancarios Sociedad
2024-03
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv


from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse


#from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base

#from typing import  Optional, List
from typing import  List
from config.database import Session


# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token

# importamos el controlador 
from controller.bancarios_sociedad import BancariosSociedadController


#importamos elschema de datos bancario del usuario
from schemas.bancarios_sociedad import BancarioSociedad as BancarioSociedadSchema




#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


#cargamos las variables de entorno
dotenv.load_dotenv()

# esta variable define al router
bancarios_sociedad_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancarios Sociedad ------------
# ruta para crear las los datos bancarios de la sociedad
@bancarios_sociedad_router.post ('/create_bancarios_sociedad', 
tags=["Bancarios Sociedad"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo el data Bancario del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el data Bancario del usuario en el sistema",
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
def create_bancarios_sociedad(bancarioSociedad:BancarioSociedadSchema,userCreatorId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=BancariosSociedadController(db).create_bancario_sociedad(bancarioSociedad,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newBancarioSociedadId=result["newBancarioSociedadId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el dato Bancario de la sociedad en el sistema","newBancarioSociedadId":newBancarioSociedadId})       
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})  
    
    


# ruta para consultar los datos Bancarios de un usuario
@bancarios_sociedad_router.get ('/bancarios_sociedad/{id}', 
tags=["Bancarios Sociedad"],
status_code=200, 
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos bancarios de la sociedad",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos bancarios de la sociedad",
                            "data":"{'id': '1','sociedad_id': '1','banco_id': '1','numero_cuenta': '0102002','codigo_convenio': '','giro_empresa': '','razon_social': '','ocultar_email': '1','created': '2024-03-21T09:10:05',   'updated':'2024-03-21T09:10:05','creator_user':'1', 'updater_user':'1'}"
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
def get_bancarios_sociedad(id: int = Path (ge=1,le=1000)):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = BancariosSociedadController(db).get_bancario_sociedad(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']        
        return JSONResponse(status_code=200,content={"Bancarios Sociedad":jsonable_encoder(data)})    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        


# ruta para consultar el historial de los datos  Bancarios de un usuario
@bancarios_sociedad_router.get ('/bancarios_sociedad/{id}/list_historicos', 
tags=["Bancarios Sociedad"],
status_code=200, 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos bancarios de la sociedad",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos bancarios de la sociedad",
                            "data":"{'id': '1','sociedad_id': '1','banco_id': '1','numero_cuenta': '0102002','codigo_convenio': '','giro_empresa': '','razon_social': '','ocultar_email': '1','created': '2024-03-21T09:10:05','updated':'2024-03-21T09:10:05','creator_user':'1', 'updater_user':'1','fecha_reegistro':'2024-03-21T09:10:05','observaciones':'prueba'}"
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
async  def get_historico_bancarios_sociedad(id : int = Path (ge=1,le=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = BancariosSociedadController(db).list_history_bancario_sociedad(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content=jsonable_encoder(data))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para actualizar los datos Bancarios de un Usuario
@bancarios_sociedad_router.put ('/bancarios_sociedad/{id}/update', 
tags=["Bancarios Sociedad"],
status_code=200, 
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
def update_bancarios_sociedad(bancarioSociedad:BancarioSociedadSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int= Path(ge=1, le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = BancariosSociedadController(db).update_bancario_sociedad(user_updater, bancarioSociedad,id) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Registro actualizado"})    
    elif (result['result']=="-2"):
        return JSONResponse(status_code=404,content={"message":f"Registro no encontrado {result['estado']}"}) 
    else:
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {result['error']}"})      
