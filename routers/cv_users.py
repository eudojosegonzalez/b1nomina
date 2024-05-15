'''
Rutas de CV de usuario
Created: 2024-04
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
from controller.cv_users import CVUserController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
cv_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas CV Usuario ------------

# Funcion para subir CV del profile de un usuario
@cv_user_router.post ('/user/{id}/upload_cv_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un CV de usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un CV de usuario al sistema",
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
            "description": "Tipo de archivo no permitido",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Tipo de archivo no permitido",
                            "estado":"System Error"
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
                            "estado":"System Error"
                        }
                    } 
                }       
            },
        523: {
            "description": "El usuario ya posee una CV",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El usuario ya posee una CV",
                            "estado":"System Error"
                        }
                    } 
                }       
            },
    })
async def cv_upload_user(creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),File : UploadFile=File())->dict:
    db = Session()
    result=CVUserController(db).upload_cv_user(creatorUserId,id,File)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newCVUserId=result["newCVUserId"]
        return JSONResponse (status_code=201,content={"message":"Se subió un CV de usuario al sistema","newCVUserId":newCVUserId})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})    
    elif  (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})   
    elif  (estado=="-4"):
        CVUser=result['CVUser']
        return JSONResponse (status_code=523,content={"message":"El usuario ya posee una CV","CVUser":CVUser})          
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})
    


# Funcion para subir CV del profile de un usuario
@cv_user_router.post ('/user/{id}/edit_cv_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un CV de usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un CV de usuario al sistema",
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
            "description": "Tipo de archivo no permitido",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Tipo de archivo no permitido",
                            "estado":"System Error"
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
                            "estado":"System Error"
                        }
                    } 
                }       
            },
        523: {
            "description": "El usuario no posee una CV",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El usuario ya posee una CV",
                            "estado":"System Error"
                        }
                    } 
                }       
            },
    })
async def cv_edit_user(creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),File : UploadFile=File())->dict:
    db = Session()
    result=CVUserController(db).edit_cv_user(creatorUserId,id,File)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        cvUser=result["cvUser"]
        return JSONResponse (status_code=201,content={"message":"Se subió un CV de usuario al sistema","cvUser":jsonable_encoder(cvUser)})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=523,content={"message":"El usuario no posee un CV"})    
    elif  (estado=="-5"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})   
    elif  (estado=="-4"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})              
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    



# Funcion para consultar los datos de un archivo de un usuario
@cv_user_router.get ('/user/{id}/get_cv_user',
 tags=['Usuarios'],
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
def get_cv_user(id:int = Path(ge=1, le=os.getenv("MAX_FILES_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CVUserController(db).get_cv_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para eliminar CV del profile de un usuario
@cv_user_router.delete ('/user/{id}/delete_cv_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un CV de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un CV de usuarios al sistema",
                            "newCVUserId":"1"
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
def cv_delete_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CVUserController(db).delete_cv_user(creatorUserId,id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['estado']
            return JSONResponse(status_code=201,content=jsonable_encoder(data))    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=521,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  



# Funcion para descartar CV del profile de un usuario
@cv_user_router.put ('/user/{id}/skip_cv_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se descartó un CV de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se descartó un CV de usuarios al sistema",
                            "newCVUserId":"1"
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
def cv_skip_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")), creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CVUserController(db).skip_cv_user(id,creatorUserId)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            CVUser=result['resultado']
            return JSONResponse(status_code=201,content={"message":"Se descarto la subida CV de usuario al sistema","CVUser":CVUser})    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=521,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"}) 



# Funcion para activar CV del profile de un usuario
@cv_user_router.put ('/user/{id}/activate_cv_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se activo la carga de CV de un usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se activo la carga de CV de un usuario al sistema",
                            "newCVUserId":"1"
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
def cv_activate_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")), creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = CVUserController(db).activate_cv_user(id,creatorUserId)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            CVUser=result['resultado']
            return JSONResponse(status_code=201,content={"message":"Se activó la subida CV de usuario al sistema","CVUser":CVUser})    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=521,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"}) 