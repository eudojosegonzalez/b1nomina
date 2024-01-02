
from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta


from fastapi_pagination import Page, add_pagination,paginate
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate




#from typing import  Optional, List
from typing import  List
# importamos desde la configuracion de la Base de datos las clases
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder

#importamos la libreria para generar el token y validarlo
import jwt 
from utils.jwt_managr import create_token,validate_token

# importamos el controlador 
from controller.users import userController
from models.view_general_user import ViewGeneralUser

# importamos la utilidad para generar el hash del password
from utils.hasher import hash_password,verify_password


# esto importa la tabla desde la definiciones de modelos
from models.user import Usuario as UsuarioModel
#importamos el esquema de datos para utilizarlo como referencia de datos a la hora de capturar data
from schemas.user import User


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# importamos la configuracion de la base de datos
from config.database import Session


# esta variable define al router
user_router = APIRouter(prefix="/V1.0")


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
@user_router.post ('/create_user',
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
        return JSONResponse (status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})             



@user_router.get('/users', 
tags=['Usuarios'],
response_model=Page[ViewGeneralUser])
def get_users():
    db = Session()
    return JSONResponse(paginate(db, select(ViewGeneralUser)))



# Funcion para consultar listar los datos personales de los usuarios del sistema
@user_router.get ('/list_users',
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
    }
)
def list_user():
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).list_users()
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})


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
        }    
)
def get_user(id:int = Path(ge=1, le=2000)):
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
    }
)
def update_user(usuario:User)->dict:
    userId=usuario.id
    db = Session()
    # buscamos el registro
    result = userController(db).update_user(userId,usuario) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=501,content={"message":"Ocurrió un error que no pudo ser controlado"})            



#Bulk Load
# Funcion para crear los datos personles de un usuario
@user_router.post ('/bulk_load_user',
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
def bulk_load_user(usuario:User)->dict:
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



add_pagination(user_router)  # important! add pagination to your app
