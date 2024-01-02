'''
Rutas de usuario
Created: 2023-12
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv

from fastapi import APIRouter,Body,File, UploadFile ,Path,Query, Depends, Request
from fastapi.staticfiles import StaticFiles
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
#from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse


from datetime import datetime,timedelta


#from typing import  Optional, List
from typing import  List
# importamos desde la configuracion de la Base de datos las clases
from config.database import Session



#importamos la libreria para generar el token y validarlo
import jwt 
from utils.jwt_managr import create_token,validate_token


# importamos el controlador 
from controller.users import userController


# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password,verify_password


# esto importa la tabla desde la definiciones de modelos
from models.user import Usuario as UsuarioModel
from models.view_general_user import ViewGeneralUser
#importamos el esquema de datos para utilizarlo como referencia de datos a la hora de capturar data
from schemas.user import User


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session

#cargamos las variables de entorno
dotenv.load_dotenv()

# esta variable define al router
user_router = APIRouter(prefix="/V1.0")

'''
============================ rutas POST =================================================================
'''
# metodo que logea compara el email y la clave enviadas desde  el formulario
# se crea el token si la claeve y el usuario coinciden
@user_router.post("/login", tags=["Auth"])
def login(username : str = Body, password : str = Body):
    session = Session()
    # generamos el hash del password del usuario desde la peticion HTTP
    passWord=hash_password(password)
    
    #buscamos el usuario
    userVerified = session.query(UsuarioModel).filter(UsuarioModel.username == username).first()
    
    # existe el usuario
    if (userVerified):
        #retornamos el password del usuario desde la tabla
        hashV=userVerified.password
        #comparamos los password
        autorized=verify_password(password,hashV)
        #determinamos si el usuario está activo
        userActive=userVerified.activo
        #verificamos que esta autorizado 
        if (autorized):
            #verificamos que esta activo 
            if (userActive):
                # calculamos el tiempo de expiracion del token por defecto 30 minutos
                # Define la duración en minutos
                duration_in_minutes = 120

                # Crea un objeto datetime con la hora actual
                now = datetime.now()

                # Crea un objeto timedelta
                delta = timedelta(minutes=duration_in_minutes)

                # Suma el timedelta a la hora actual
                future_time = now + delta

                timestamp_unix = future_time.timestamp()

                # creamos un diccionario para generar el token del usuario
                userDict={"username":username,"password":password,"exp":timestamp_unix}
                # generamos el token del usuario
                token: str = create_token(userDict)
                            
                return JSONResponse (status_code=202,content={"token":token,"userId":userVerified.id})
            else:
                #usuario suspendido
                return JSONResponse (status_code=401,content={"message":"Usuario suspendido"}) 
        else:
            # 
            if (not userActive):
                return JSONResponse (status_code=401,content={"message":"Usuario no autorizado"})               
    
    return JSONResponse (status_code=401,content={"message":"Usuario no autorizado"})      



@user_router.post("/validate", tags=["Auth"])
def validate(token : str = Body):
    if (validate_token(token)):
        return JSONResponse (status_code=201,content={"message":"autorizado"})   
    else:
        return JSONResponse (status_code=401,content={"message":"mo autorizado"})
    

# Funcion para crear los datos personles de un usuario
@user_router.post ('/user/create_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se creo el usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el usuario en el sistema",
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
        409: {
            "description": "Este Username ya fue registrado en el sistema, no puede volver a insertarlo",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo",
                            "userId":"1",
                             "userName":"anyUsername"
                        }
                    } 
                }       
            },
        422: {
            "description": "Este RUT ya fue registrado en el sistema, no puede volver a insertarlo",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo",
                            "userId":"1",
                            "rut":"123456789"
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


    })
def create_user(usuario:User)->dict:
    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})             


# Funcion para crear los datos personles de usuarios desde un archivo
@user_router.post ('/user/bulk_load_users',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se crearon usuarios en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se crearon usuarios en el sistema",
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
        409: {
            "description": "Se insertaron usuarios pero ocurrieron problemas al insertar algunos de los registros, \
                por favor revice las causas en el listado de estados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Se insertaron usuarios pero ocurrieron problemas al insertar algunos de los \
                                registros, por favor revice las causas en el listado de estados",
                            "processed":"n",
                            "aggregates":"n",
                            "rejected":"m",                            
                             "status":"{['rut':'1232333-8','results':'aggregate','status':'200'],\
                                ['rut':'5555555-8','results':'refused':'422'],['rut':'66666666-2','results':'refused':'422']}"
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
        501: {
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
def bulk_load_users():
    '''    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})       '''
    return JSONResponse (status_code=200,content={"message":"En desarrollo"})     


# Funcion para subir archivos al profile de un usuario
@user_router.post ('/user/{id}/upload_file_users',
tags=['Usuarios'],
#dependencies=[Depends(JWTBearer())], 
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
async def file_upload_user(creatorUserId : int = Query (ge=1, lt=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, lt=os.getenv("MAX_ID_USERS")),file : UploadFile=File())->dict:
    db = Session()
    result=userController(db).upload_file_user(creatorUserId,id,file)
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


# Funcion para subir foto del profile de un usuario
@user_router.post ('/user/{id}/upload_pic_user',
tags=['Usuarios'],
#dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió una imagen de usuario al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió una imagen de usuario al sistema",
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
            "description": "El usuario ya posee una foto",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"El usuario ya posee una foto",
                            "estado":"System Error"
                        }
                    } 
                }       
            },
    })
async def pic_upload_user(creatorUserId : int = Query (ge=1, lt=os.getenv("MAX_ID_USERS")) ,id : int = Path (ge=1, lt=os.getenv("MAX_ID_USERS")),file : UploadFile=File())->dict:
    db = Session()
    result=userController(db).upload_pic_user(creatorUserId,id,file)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newPicUserId=result["newPicUserId"]
        return JSONResponse (status_code=201,content={"message":"Se subió una imagen de usuario al sistema","newPicUserId":newPicUserId})     
    elif  (estado=="-1"):
        return JSONResponse (status_code=521,content={"message":"Tipo de archivo no permitido","estado":result})    
    elif  (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"El archivo es demasiado grande","estado":result})   
    elif  (estado=="-4"):
        picUser=result['picUser']
        return JSONResponse (status_code=523,content={"message":"El usuario ya posee una foto","picUser":picUser})          
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})



# Funcion para eliminar archivos al profile de un usuario
@user_router.post ('/user/associate_user_company',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se asoció un usuario a una sociedad",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se asoció un usuario a una sociedad",
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
          501: {
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
def associate_user_company():
    '''    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})       '''
    return JSONResponse (status_code=200,content={"message":"En desarrollo"}) 


'''
============================ rutas GET =================================================================
'''
# Funcion para consultar listar los datos personales de los usuarios del sistema
@user_router.get ('/user/list_users',
tags=['Usuarios'],
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
async def list_users(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).list_users(page,records)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})
   
    
# Funcion para efectuar busquedas en la vista viewGeneralUser
# se efectuan busquedas del tipo LIKE en la vista
@user_router.get ('/user/search',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Usuario encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Usuario encontrado",
                                    "data": "{'id':'1','rut': '12345678912','rut': '12345678912', 'nombres': 'Pedro ', 'apellido_paterno': 'Perez', 'apellido_materno': 'Martinez', 'fecha_nacimiento': '1990-01-01','sexo_id': '1', 'estado_civil_id': '1', 'nacionalidad_id': '1','username': 'pperez' 'password': '12345678','activo':'1','created':'1990-01-01 10:00','updated':'1990-01-01 11:00','creator_user':'1','updater_user':'1' }",
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
async def search_users(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")), page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).search_users(finding,page,records)
    # debemnos convertir los objetos tipo BD a Json
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


# Funcion para consultar los datos personales de un usuario
@user_router.get (
    '/user/{id}',
    tags=['Usuarios'],
    dependencies=[Depends(JWTBearer())],
    responses=
        { 
            200: {
                    "description": "Usuario encontrado",
                    "content": { 
                        "application/json":
                            { 
                                "example":
                                    {
                                        "message":"Usuario encontrado",
                                        "data": "{'id':'1','rut': '12345678912','rut': '12345678912', 'nombres': 'Pedro ', 'apellido_paterno': 'Perez', 'apellido_materno': 'Martinez', 'fecha_nacimiento': '1990-01-01','sexo_id': '1', 'estado_civil_id': '1', 'nacionalidad_id': '1','username': 'pperez' 'password': '12345678','activo':'1','created':'1990-01-01 10:00','updated':'1990-01-01 11:00','creator_user':'1','updater_user':'1' }",
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
                "description": "Usuario no encontrado",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Usuario no encontrado"
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
def get_user(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para consultar el historico de los datos personales de un usuario
@user_router.get (
    '/user/{id}/history_data_personal',
    tags=['Usuarios'],
    dependencies=[Depends(JWTBearer())],
    responses=
        { 
            200: {
                    "description": "Usuario encontrado",
                    "content": { 
                        "application/json":
                            { 
                                "example":
                                    {
                                        "message":"Usuario encontrado",
                                        "data": "{'id':'1','rut': '12345678912','rut': '12345678912', 'nombres': 'Pedro ', 'apellido_paterno': 'Perez', 'apellido_materno': 'Martinez', 'fecha_nacimiento': '1990-01-01','sexo_id': '1', 'estado_civil_id': '1', 'nacionalidad_id': '1','username': 'pperez' 'password': '12345678','activo':'1','created':'1990-01-01 10:00','updated':'1990-01-01 11:00','creator_user':'1','updater_user':'1' }",
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
                "description": "Usuario no encontrado",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Usuario no encontrado"
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
def get_user_history_data_personal(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_user_history_data_personal(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  



# Funcion para consultar los datos de un archivo de un usuario
@user_router.get (
    '/user/get_file_user/{id}',
    tags=['Usuarios'],
#dependencies=[Depends(JWTBearer())],
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
    result = userController(db).get_file_user(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Archivo no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para listar los archivos de un usuario del sistema, se filtra por ID de usuario
@user_router.get ('/user/{id}/list_files_users',
tags=['Usuarios'],
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
async def list_files_users(id: int = Path (ge=1, lt=os.getenv("MAX_ID_USERS")),page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).list_files_users(id,page,records)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})    



'''
============================ rutas PUT =================================================================
'''
# Función para actualizar  los datos personales un usuario
@user_router.put ('/user/{id}/update',
tags=['Usuarios'],
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
def update_user(user_updater: int, usuario:User):
    db = Session()
    # buscamos el registro
    result = userController(db).update_user(user_updater,usuario) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})          


# Función para activar un usuario
@user_router.put ('/user/{id}/activate_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Se activó al usuario",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Se activó al usuario"
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
def activate_user(user_updater: int, usuario:User):
    db = Session()
    # buscamos el registro
    result = userController(db).activate_user(user_updater,usuario) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  
    

# Función para desactivar al usuario
@user_router.put ('/user/{id}/deactivate_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Se desactivó al usuario",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Se desactivó al usuario"
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
def deactivate_user(user_updater: int, usuario:User):
    db = Session()
    # buscamos el registro
    result = userController(db).deactivate_user(user_updater,usuario) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  
    


# Función para actualizar  la clave de un usuario
@user_router.put ('/user/{id}/update_password',
tags=['Usuarios'],
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
def update_password_user(id , user_updater: int, password:str):
    db = Session()
    # buscamos el registro
    result = userController(db).update_password_user(id,user_updater, password) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Password de Usuario Actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  
    

# Funcion para subir foto del profile de un usuario
@user_router.put ('/user/update_pic_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió una imagen de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió una imagen de usuarios al sistema",
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
    })
def pic_update_user():
    '''    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})       '''
    return JSONResponse (status_code=200,content={"message":"En desarrollo"}) 



'''
============================ rutas DELETE =================================================================
'''
# Funcion para eliminar foto del profile de un usuario
@user_router.delete ('/user/delete_pic_user',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se subió una imagen de usuarios al sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se subió una imagen de usuarios al sistema",
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
        501: {
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
def pic_delete_user():
    '''    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})       '''
    return JSONResponse (status_code=200,content={"message":"En desarrollo"}) 


# Funcion para eliminar archivos al profile de un usuario
@user_router.delete ('/user/delete_file_users',
tags=['Usuarios'],
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
          501: {
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
def file_delete_user():
    '''    db = Session()
    result=userController(db).create_user(usuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif  (estado=="-2"):
        # el username ya existe no puede volver a insertarlo
        userId=result["userId"]
        userName=result["userName"]
        return JSONResponse (status_code=409,content={"message":"Este Username ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"userName":userName})     
    elif (estado=="-3"):
        userId=result["userId"]
        rut=result["rut"]
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","userId":userId,"rut":rut})     

    else:
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})       '''
    return JSONResponse (status_code=200,content={"message":"En desarrollo"}) 




