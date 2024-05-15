'''
Rutas de Contrato de usuario
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
from controller.contrato_users import ContratoUserController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
contrato_user_router = APIRouter(prefix="/V1.0")

# -------- Rutas Contrato Usuario ------------

# Funcion para subir Contrato del profile de un usuario
@contrato_user_router.post ('/user/{id}/upload_contrato_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un Contrato de usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un Contrato de usuario al sistema",
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
            "description": "El usuario ya posee una Contrato",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El usuario ya posee una Contrato",
                            "estado":"System Error"
                        }
                    } 
                }       
            },
    })
async def contrato_upload_user(creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),File : UploadFile=File())->dict:
    db = Session()
    result=ContratoUserController(db).upload_contrato_user(creatorUserId,id,File)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newContratoUserId=result["newContratoUserId"]
        return JSONResponse (status_code=201,content={"message":"Se subió un Contrato de usuario al sistema","newContratoUserId":newContratoUserId})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})    
    elif  (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})   
    elif  (estado=="-4"):
        ContratoUser=result['ContratoUser']
        return JSONResponse (status_code=523,content={"message":"El usuario ya posee una Contrato","ContratoUser":ContratoUser})          
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})


# Funcion para editar Contrato del profile de un usuario
@contrato_user_router.post ('/user/{id}/edit_contrato_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un Contrato de usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un Contrato de usuario al sistema",
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
            "description": "El usuario no posee una Contrato",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El usuario no posee una Contrato",
                            "estado":"System Error"
                        }
                    } 
                }       
            },
    })
async def contrato_edit_user(creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),File : UploadFile=File())->dict:
    db = Session()
    result=ContratoUserController(db).edit_contrato_user(creatorUserId,id,File)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        contratoUser=result["contratoUser"]
        return JSONResponse (status_code=201,content={"message":"Se subió un Contrato de usuario al sistema","ContratoUser":jsonable_encoder(contratoUser)})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=523,content={"message":"El usuario no posee un contrato"})    
    elif  (estado=="-5"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})   
    elif  (estado=="-4"):
        permitidos=result['permitidos']
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","permitidos":jsonable_encoder(permitidos)})              
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    


# Funcion para consultar los datos de un archivo de un usuario
@contrato_user_router.get ('/user/{id}/get_contrato_user',
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
def get_contrato_user(id:int = Path(ge=1, le=os.getenv("MAX_FILES_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ContratoUserController(db).get_contrato_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para eliminar Contrato del profile de un usuario
@contrato_user_router.delete ('/user/{id}/delete_contrato_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió un Contrato de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió un Contrato de usuarios al sistema",
                            "newContratoUserId":"1"
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
def contrato_delete_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ContratoUserController(db).delete_contrato_user(creatorUserId,id)
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



# Funcion para descartar Contrato del profile de un usuario
@contrato_user_router.put ('/user/{id}/skip_contrato_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se descartó un Contrato de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se descartó un Contrato de usuarios al sistema",
                            "newContratoUserId":"1"
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
def contrato_skip_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")), creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ContratoUserController(db).skip_contrato_user(id,creatorUserId)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            ContratoUser=result['resultado']
            return JSONResponse(status_code=201,content={"message":"Se descarto la subida Contrato de usuario al sistema","ContratoUser":ContratoUser})    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=521,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"}) 



# Funcion para activar Contrato del profile de un usuario
@contrato_user_router.put ('/user/{id}/activate_contrato_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se activo la carga de Contrato de un usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se activo la carga de Contrato de un usuario al sistema",
                            "newContratoUserId":"1"
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
def contrato_activate_user(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")), creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = ContratoUserController(db).activate_contrato_user(id,creatorUserId)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            ContratoUser=result['resultado']
            return JSONResponse(status_code=201,content={"message":"Se activó la subida de Contrato de usuario al sistema","ContratoUser":ContratoUser})    
        elif (result["result"]=="-3"):
            data=result["estado"]
            return JSONResponse(status_code=521,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
   
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"}) 