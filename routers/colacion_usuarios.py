'''
Rutas de Colacion Usuarios
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
from controller.colacion_usuarios import ColacionUsuariosController


#importamos elschema de datos bancario del usuario
from schemas.colacion_usuarios import ColacionUser as ColacionUserSchema




#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


#cargamos las variables de entorno
dotenv.load_dotenv()

# esta variable define al router
colacion_usuarios_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancarios Usuarios ------------
# ruta para crear las los datos bancarios del usuario
@colacion_usuarios_router.post ('/create_colacion_user', 
tags=["Colacion Usuarios"], 
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo los datos de Colacion del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo los datos de Colacion del usuario en el sistema",
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
def create_colacion_user(colacionUsuario:ColacionUserSchema,userCreatorId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=ColacionUsuariosController(db).create_colacion_user(colacionUsuario,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newColacionId=result["newColacionId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el dato de Colación del Usuario en el sistema","newColacionId":newColacionId})       
    elif (estado=="-1"):
        # ya existe los datos de colacion n o puede volver a crearlos
        return JSONResponse (status_code=200,content={"message":"Este usuario ya tiene datos de Colación en el sistema no puede volver a crearlos"})
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})  
    

   


# ruta para consultar los datos de Colación de un usuario
@colacion_usuarios_router.get ('/colacion_user/{id}', 
tags=["Colacion Usuarios"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos de Colacion del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos de Colacion del usuario",
                              "data":"{'id': '1','colacion_usuario_id': '1','sociedad_id': '1','user_id': '1','colacion': '10000', 'movilizacion': '30000','familiar': '2000','created': '2024-03-22T13:49:13', 'updated': '2024-03-22T13:49:13','creator_user': '1','updater_user': '1'}"
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
def get_colacion_user(id: int = Path (ge=1,le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ColacionUsuariosController(db).get_colacion_user(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']        
        return JSONResponse(status_code=200,content={"Colacion Usuario":jsonable_encoder(data)})    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        


# ruta para consultar el historial de los datos  Bancarios de un usuario
@colacion_usuarios_router.get ('/colacion_user/{id}/list_historicos', 
tags=["Colacion Usuarios"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Datos de Colacion del usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Datos de Colacion del usuario",
                             "data":"{'id': '1','colacion_usuario_id': '1','sociedad_id': '1','user_id': '1','colacion': '10000', 'movilizacion': '30000','familiar': '2000','created': '2024-03-22T13:49:13', 'fecha_registro': '2024-03-22T13:49:13','updated': '2024-03-22T13:49:13','creator_user': '1','updater_user': '1','observaciones': 'Se creó los datos de colacion del usuario'}"
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
async  def get_historico_colacion_user(id : int = Path (ge=1,le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ColacionUsuariosController(db).list_history_colacion_user(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content=jsonable_encoder(data))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para actualizar los datos de Colación de un Usuario
@colacion_usuarios_router.put ('/colacion_user/{id}/update', 
tags=["Colacion Usuarios"],
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
def update_colacion_user(colacionUser:ColacionUserSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = ColacionUsuariosController(db).update_colacion_user(user_updater, colacionUser) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Registro actualizado"})    
    elif (result['result']=="-2"):
        return JSONResponse(status_code=404,content={"message":f"Registro no encontrado {result['estado']}"}) 
    else:
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {result['error']}"})      
