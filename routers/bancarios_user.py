'''
Rutas de Bancarios Usuarios
2024-01
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
from controller.bancarios_users import bancariosUserController


#importamos elschema de datos bancario del usuario
from schemas.bancarios_user import BancarioUser as BancariosUserSchema




#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


#cargamos las variables de entorno
dotenv.load_dotenv()

# esta variable define al router
bancarios_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancarios Usuarios ------------
# ruta para crear las los datos bancarios del usuario
@bancarios_user_router.post ('/create_bancarios_user', 
tags=["Bancarios Usuarios"], 
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
def create_bancarios_user(bancarioUsuario:BancariosUserSchema,userCreatorId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=bancariosUserController(db).create_bancario_user(bancarioUsuario,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newBancarioUserId=result["newBancarioUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el dato Bancario del Usuario en el sistema","newBancarioUserId":newBancarioUserId})       
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})  
    

# ruta para listar los datos bancarios de todos los usuarios
@bancarios_user_router.get ('/list_bancarios_user', 
tags=["Bancarios Usuarios"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Listado de Datos Bancarios de los Usuarios",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Listado de Datos Bancarios de los Usuarios",
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
async def list_bancarios_users(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = bancariosUserController(db).list_bancarios_users(page,records)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    


# ruta para consultar los datos Bancarios de un usuario
@bancarios_user_router.get ('/user/{id}/bancarios', 
tags=["Usuarios"],
status_code=200, 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Datos bancarios del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos bancarios del usuario",
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
def get_bancarios_user(id: int = Path (ge=1,le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = bancariosUserController(db).get_bancario_user(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']        
        return JSONResponse(status_code=201,content={"BancariosdelUsuario":jsonable_encoder(data)})    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        


# ruta para consultar el historial de los datos  Bancarios de un usuario
@bancarios_user_router.get ('/user/{id}/list_historicos_bancarios', 
tags=["Bancarios Usuarios"],
status_code=200, 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Datos bancarios del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos bancarios del usuario",
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
async  def get_historico_bancarios_user(id : int = Path (ge=1,le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = bancariosUserController(db).list_history_bancario_user(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content=jsonable_encoder(data))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para actualizar los datos Bancarios de un Usuario
@bancarios_user_router.put ('/user/{id}/update_bancarios', 
tags=["Bancarios Usuarios"],
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
def update_bancarios_user(bancarioUser:BancariosUserSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = bancariosUserController(db).update_bancario_user(user_updater, bancarioUser) 
    if (result['result']=="1"):
        return JSONResponse(status_code=201,content={"message":"Registro actualizado"})    
    elif (result['result']=="-2"):
        return JSONResponse(status_code=404,content={"message":f"Registro no encontrado {result['estado']}"}) 
    else:
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {result['error']}"})      
