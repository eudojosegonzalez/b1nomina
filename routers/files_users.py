'''
Rutas de Archivos de usuario
Created: 2023-12
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv


from fastapi import File, UploadFile
from fastapi import APIRouter
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse


# importamos desde la configuracion de la Base de datos las clases
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder


# importamos el controlador 
from controller.files_users import FilesUserController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
files_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Archivos Usuario ------------
# Funcion para subir archivos al profile de un usuario
@files_user_router.post ('/user/{id}/upload_file_users',
tags=['Archivos de Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un archivo de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un archivo de usuarios al sistema",
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
            "description": "Tipo de archivo no permitido",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Tipo de archivo no permitido",
                            'Archivos Permitidos': ['png','jpg','jpeg','gif','pdf']
                        }
                    } 
                }       
            }, 
          522: {
            "description": "El archivo es demasiado grande",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El archivo es demasiado grande",
                            "estado":"El archivo es demasiado grande, tamaño máximo permitido 20Mb"
                        }
                    } 
                }       
            },                                             
    })
async def file_upload_user(creatorUserId:int = Query(ge=1, le=os.getenv("MAX_ID_USERS")), id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")), file: UploadFile=File())->dict:
    db = Session()
    result=FilesUserController(db).upload_file_user(creatorUserId,id,file)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newFileUserId=result["newFileUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el archivo del usuario en el sistema","newfileUserId":newFileUserId})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})    
    elif  (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})        
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})



# Funcion para consultar los datos de un archivo de un usuario
@files_user_router.get (
 '/user/get_file_user/{id}/',
tags=['Archivos de Usuarios'],
dependencies=[Depends(JWTBearer())],
 responses=
        { 
            200: {
                    "description": "Archivo encontrado",
                    "content": { 
                        "application/json":
                            { 
                                "example":
                                    {
                                        "message":"Usuario encontrado",
                                        "data": "{'id':'1','user_id':'1','nombre':'archivo.jpg','url':'/files_users/archivo.jpg','created':'1990-01-01 10:00','updated':'1990-01-01 11:00','creator_user':'1','updater_user':'1' }",
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
                "description": "Archivo no encontrado",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Archivo no encontrado"
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
def get_file_user(id:int = Path(ge=1, le=os.getenv("MAX_FILES_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = FilesUserController(db).get_file_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  



# Funcion para listar los archivos de un usuario del sistema, se filtra por ID de usuario
@files_user_router.get ('/user/{id}/list_files_users',
tags=['Archivos de Usuarios'],
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
    }
)
async def list_files_users(id: int = Path (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = FilesUserController(db).list_files_users(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})    



# Funcion para eliminar archivos al profile de un usuario
@files_user_router.delete ('/user/delete_file_users/{id}',
tags=['Archivos de Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un archivo de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un archivo de usuarios al sistema",
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
            "description": "No se pudo elimiar el registro",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"No se pudo elimiar el registro",
                            "estado":"System Error"
                        }
                    } 
                }       
            },           
        521: {
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


    })
def file_delete_user(id : int = Path (ge=1, le=20000)):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = FilesUserController(db).delete_file_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['estado']
            return JSONResponse(status_code=201,content=jsonable_encoder(data))    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=520,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=521,content={"message":"Ocurrió un error que no pudo ser controlado"})  


