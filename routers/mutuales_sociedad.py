'''
Rutas de Mutuales Sociedad
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
from controller.mutuales_sociedad import MutualesSociedadController


#importamos elschema de datos mutuales de una sociedad
from schemas.mutuales_sociedad import MutalesSociedad as MutualesSociedadSchema




#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


#cargamos las variables de entorno
dotenv.load_dotenv()

# esta variable define al router
mutuales_sociedad_router = APIRouter(prefix="/V1.0")

# -------- Rutas Mutuales Sociedad ------------
# ruta para crear las los datos mutuales de la sociedad
@mutuales_sociedad_router.post ('/create_mutuales_sociedad', 
tags=["Mutuales Sociedad"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo el dato Mutual del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"e creo el dato Mutual del usuario en el sistema",
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
def create_mutuales_sociedad(mutualSociedad:MutualesSociedadSchema,userCreatorId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=MutualesSociedadController(db).create_mutual_sociedad(mutualSociedad,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newMutualSociedadId=result["newMutualSociedadId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el dato Mutual de la sociedad en el sistema","newMutualSociedadId":newMutualSociedadId})       
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})  
    
    


# ruta para consultar los datos Mutuales de una sociedad
@mutuales_sociedad_router.get ('/mutuales_sociedad/{id}', 
tags=["Mutuales Sociedad"],
status_code=200, 
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos mutuales de la sociedad",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos mutuales de la sociedad",
                            "data":"{'id': 1,'sociedad_id': 1,'mutual_id': 7, 'porcentaje': 0.4,'created':'2024-03-21T11:06:08','updated': '2024-03-21T11:06:08','creator_user': 1,'updater_user': 1}"
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
def get_mutuales_sociedad(id: int = Path (ge=1,le=1000)):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = MutualesSociedadController(db).get_mutual_sociedad(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']        
        return JSONResponse(status_code=201,content={"Mutuales Sociedad":jsonable_encoder(data)})    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        


# ruta para consultar el historial de los datos  Mutuales de un usuario
@mutuales_sociedad_router.get ('/mutuales_sociedad/{id}/list_historicos', 
tags=["Mutuales Sociedad"],
status_code=200, 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos mutuales de la sociedad",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos mutuales de la sociedad",
                            "data":"{'id': 1,'sociedad_id': 1,'mutual_id': 7, 'porcentaje': 0.4,'created':'2024-03-21T11:06:08','updated': '2024-03-21T11:06:08','creator_user': 1,'updater_user': 1,'fecha_registro':'2024-03-21T11:06:08','observaciones':''}"
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
async  def get_historico_mutuales_sociedad(id : int = Path (ge=1,le=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = MutualesSociedadController(db).list_history_mutual_sociedad(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content=jsonable_encoder(data))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para actualizar los datos Mutuales de una Scoiedad
@mutuales_sociedad_router.put ('/mutuales_sociedad/{id}/update', 
tags=["Mutuales Sociedad"],
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
def update_mutuales_sociedad(mutualSociedad:MutualesSociedadSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id: int = Path(ge=1, le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = MutualesSociedadController(db).update_mutual_sociedad(user_updater, mutualSociedad,id) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Registro actualizado"})    
    elif (result['result']=="-2"):
        return JSONResponse(status_code=404,content={"message":f"Registro no encontrado {result['estado']}"}) 
    else:
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {result['error']}"})      
