'''
Rutas de usuario
Created: 2023-12
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv

from fastapi import APIRouter,Body,Path,Query, Depends
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
#from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
from fastapi import  Request
from fastapi import File, UploadFile


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
from schemas.login import Login
from schemas.preregistro_user import PreUser as PreUserSchema
from schemas.preregistro_user2 import PreUser2 as PreUser2Schema
from schemas.usuarios_grupo import UsuariosGruposEmpleado as UsuariosGruposEmpleadoSchema
from schemas.contratados import Contratados as ContratadosSchema
from schemas.datos_laborales_salario import DatosLaboralesSalario as DatosLaboralesSalarioSchema
from schemas.datos_laborales_contrato import DatosLaboralesContrato as DatosLaboralesContratoSchema
from schemas.datos_laborales_puesto import DatosLaboralesPuesto as DatosLaboralesPuestoSchema
from schemas.datos_personales import DatosPersonales as DatosPersonalesSchema
from schemas.contact_ubication_user import ContactUbicationUser as ContactUbicationUserSchema

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
                duration_in_minutes = 3600

                # Crea un objeto datetime con la hora actual
                now = datetime.now()

                # Crea un objeto timedelta
                delta = timedelta(seconds=duration_in_minutes)

                # Suma el timedelta a la hora actual
                future_time = now + delta

                timestamp_unix = future_time.timestamp()

                # creamos un diccionario para generar el token del usuario
                userDict={"username":username,"password":password,"expires_in":timestamp_unix}
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


# metodo que logea compara el email y la clave enviadas desde  el formulario
# se crea el token si la claeve y el usuario coinciden
@user_router.post("/login2", tags=["Auth"])
def login(login:Login):
    session = Session()
    # generamos el hash del password del usuario desde la peticion HTTP
    passWord=hash_password(login.password)
    
    #buscamos el usuario
    userVerified = session.query(UsuarioModel).filter(UsuarioModel.username == login.username).first()
    
    # existe el usuario
    if (userVerified):
        #retornamos el password del usuario desde la tabla
        hashV=userVerified.password
        #comparamos los password
        autorized=verify_password(login.password,hashV)
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
                userDict={"username":login.username,"password":login.password,"exp":timestamp_unix}
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
@user_router.post ('/user/create_preuser',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se creo el preregistro del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el preregistro del usuario en el sistema",
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


    }
)
def create_preuser(preUsuario:PreUserSchema)->dict:
    db = Session()
    result=userController(db).create_pre_user(preUsuario)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif (estado=="-3"):
        userExist=jsonable_encoder(result)
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","User":userExist})    
    elif (estado=="-1"):
        cadenaErrores=result["estado"]
        return JSONResponse (status_code=521,content={"message":f"Error en los formatos de los datos, {cadenaErrores}","estado":cadenaErrores})       
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    



# Funcion para crear los datos personles de un usuario Formulario 2
@user_router.post ('/user/create_preuser2',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se creo el preregistro del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el preregistro del usuario en el sistema",
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


    }
)
def create_preuser2(preregistro_user2:PreUser2Schema, creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).create_pre_user2(preregistro_user2, creatorUserId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})     
    elif (estado=="-3"):
        userExist=jsonable_encoder(result)
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","User":userExist})    
    elif (estado=="-1"):
        cadenaErrores=result["estado"]
        return JSONResponse (status_code=521,content={"message":"Error en los formatos de los datos","estado":cadenaErrores})       
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})  
   


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
    }
)
def create_user(usuario:User,creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).create_user(usuario,creatorUserId)
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
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})              


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
async def bulk_load_users(sociedadId: int , creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")),File : UploadFile=File()):
    db = Session()
    result = await userController(db).upload_massive_user(sociedadId,creatorUserId,File)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        fileResult=result['fileResult']
        return JSONResponse (status_code=201,content={"message":"Se proceso una importacion masiva en el sistema","fileResult":fileResult}) 
    elif (estado=="-2"):
        return JSONResponse (status_code=522,content={"message":"Archivo no procesado"})                  
    elif (estado=="-4"):
        return JSONResponse (status_code=521,content={"message":"El archivo está vacio"})  
    elif (estado=="-3"):
        cadena=result['cadenaError']
        return JSONResponse (status_code=523,content={"message":"Ocurrio un error que no pudo ser controlado","Error":cadena})  
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  


# Funcion para asosciar un usuario a un departamento
@user_router.post ('/user/asociar_usuario_sociedad',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se asoció un usuario a departamento",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se asoció un usuario a un departamento",
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
    }
)
def associate_user_society(userGroup:UsuariosGruposEmpleadoSchema,creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).asignate_user_society(userGroup, creatorUserId )
    # evaluamos el resultado
    estado=result['result']    
    
    if (estado=="1") :
        # se inserto el registro sin problemas
        return JSONResponse (status_code=201,content={"message":"Se asoció el usuario al grupo"})     
    elif  (estado=="-2"):
        # el usuario ya esta asociado a otro grupo, no puede volver a crearlo
        data=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario esta asociado a otro grupo, no puede volver a crearlo","UsuarioGrupo":jsonable_encoder(data)})     
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})              




# Funcion para asosciar un usuario a un departamento
@user_router.post ('/user/asociar_usuario_departamento',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se asoció un usuario a departamento",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se asoció un usuario a un departamento",
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
    }
)
def associate_user_departament(userGroup:UsuariosGruposEmpleadoSchema,creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).asignate_user_departament(userGroup, creatorUserId )
    # evaluamos el resultado
    estado=result['result']    
    
    if (estado=="1") :
        # se inserto el registro sin problemas
        return JSONResponse (status_code=201,content={"message":"Se asoció el usuario al grupo"})     
    elif  (estado=="-2"):
        # el usuario ya esta asociado a otro grupo, no puede volver a crearlo
        data=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario esta asociado a otro grupo, no puede volver a crearlo","UsuarioGrupo":jsonable_encoder(data)})     
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})              


# Funcion para asosciar un usuario a un grupo
@user_router.post ('/user/asociar_usuario_grupo',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se asoció un usuario a grupo",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se asoció un usuario a un grupo",
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
    }
)
def associate_user_group(userGroup:UsuariosGruposEmpleadoSchema,creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).asignate_user_group(userGroup, creatorUserId )
    # evaluamos el resultado
    estado=result['result']    
    
    if (estado=="1") :
        # se inserto el registro sin problemas
        return JSONResponse (status_code=201,content={"message":"Se asoció el usuario al grupo"})     
    elif  (estado=="-2"):
        # el usuario ya esta asociado a otro grupo, no puede volver a crearlo
        data=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario esta asociado a otro grupo, no puede volver a crearlo","UsuarioGrupo":jsonable_encoder(data)})     
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})              


# Funcion para asosciar un usuario a un grupo
@user_router.post ('/user/contratar',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Se contrato al usuario",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se asoció un usuario a un grupo",
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
            "description": "Este usuario ya se encuentra contratado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Este usuario ya se encuentra contratado",
                            "data":"{'id':1,'sociedad_id':1,'user_id':1,'estado':1,'created':'2024-01-01 10:00','updated':'2024-01-01 10:00','creator_user':1,'updater_user:1}"
                        }
                    } 
                }       
        },          
        522: {
                "description": "No se pudo verificar el estatus de inscripcion",
                "content": { 
                    "application/json":
                        { "example":
                            {
                                "message":"No se pudo verificar el estatus de inscripcion",
                            }
                        } 
                    }       
        }, 
        523: {
            "description": "Hay data faltante para procesar la contratacion",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Hay data faltante para procesar la contratacion",
                            "data":"{'rut':'falta','nombre':'falta','apellido':'falta'}"
                        }
                    } 
                }       
        },                                     
    }
)
def contratar_user(contratado:ContratadosSchema,creatorUserId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).contratar_user(contratado, creatorUserId )
    # evaluamos el resultado
    estado=result['result']    
    
    if (estado=="1") :
        # se inserto el registro sin problemas
        data=result['data']
        return JSONResponse (status_code=201,content={"message":"Se contrato al usuario","Contratado":jsonable_encoder(data)})     
    elif  (estado=="-1"):
        # el usuario ya esta contratado
        data=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario esta contratado, no puee volver a contratarlo","Usuario Contratado":jsonable_encoder(data)})     
    elif  (estado=="-2"):
        # no se pudo verificar el estatus de inscripcion
        return JSONResponse (status_code=522,content={"message":"No se pudo verificar el estatus de inscripcion"})     
    elif  (estado=="-4"):
        # falta data para cpontratar a la persona
        data=result['data']
        return JSONResponse (status_code=523,content={"message":"Hay data faltante para procesar la contratacion","data":jsonable_encoder(data)})     
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})              



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
def   list_users(page : int = 1, records : int = 20)->dict:
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
def   search_users(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")), page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).search_users(finding,page,records)
    # debemos convertir los objetos tipo BD a Json
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
@user_router.get ('/user/{id}',
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
                                    "data": "{'id': '101','nacionalidad_id': '1','email': 'farayaaraneda@hotmail.com','rut_provisorio': '','username': '19848318-4','sociedad_id': null,'nombres': 'CAMILA IGNACIA ',   'password': '12345678','apellido_paterno': 'ALARCON ','activo': true,'apellido_materno': 'RAMIREZ','created': '2022-05-26T00:00:00','fecha_nacimiento': '1998-03-27','updated':'1990-01-01T00:01:00','sexo_id': 2,'creator_user': '1','rut': '19848318-4','estado_civil_id': 1,'updater_user': '1'}",
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




# Funcion para consultar los datos personales de un usuario
@user_router.get ('/user/{id}/datos_personales',
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
                                    "data": "{'user_id': 248,'rut': '19116452-0','nombres': 'CONSTANZA','apellido_paterno': 'QUEVEDO','fecha_nacimiento': '1995-07-06', 'sexo_id': 2, 'estado_civil_id': 1, 'nacionalidad_id': 1}",
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
    result = userController(db).get_datos_personales(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  



# Funcion para consultar los datos personales de un usuario
@user_router.get ('/user/{id}/avance_inscripcion',
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
                                    "data": "{'avance': '50'}",
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
        520: {
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
def get_user_avance(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_avance(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['avance']
            return JSONResponse(status_code=200,content={"message":"Usuario Encontrado","avance":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":f"{result['estado']}"})     
    
    
    return JSONResponse(status_code=520,content={"message":"Ocurrio un error que no pudo ser controlado"})  


# Funcion para consultar los datos personales de un usuario en precarga
@user_router.get ('/user/{id}/precarga',
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
                                    "data": "{'documento': '1','nombres': 'Admin','apellidos': 'Root','correo': 'null','nacionalidad': '1','genero': '1','fechaNacimiento': '1990-01-01','estadoCivil': '1','region': '13','localidad': '13106','direccion': 'alguna dirección dos','telefonoCelular': 'null','telefonoLocal': 'null'}",
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
    result = userController(db).get_preuser(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para consultar los datos preofile de un usuario en precarga
@user_router.get ('/user/{id}/precarga_all',
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
                                    "data": "{'documento': '1','nombres': 'Admin','apellidos': 'Root','correo': 'null','nacionalidad': '1','genero': '1','fechaNacimiento': '1990-01-01','estadoCivil': '1','region': '13','localidad': '13106','direccion': 'alguna dirección dos','telefonoCelular': 'null','telefonoLocal': 'null'}",
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
def get_profile_preuser(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_profile_preuser(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})  


# Funcion para consultar el historico de los datos personales de un usuario
@user_router.get ('/user/{id}/list_historico',
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


#funcion para determianr los modulos asignados a un usuario 
@user_router.get ('/user/{id}/asignated_modules',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
                "description": "Módulos asignados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {                           
                                    "message":"Modulos de Usuario encontrado",
                                    "data": "{'idModulo': 3,'nombreModulo': 'Eventos','urlModulo': '/eventos','iconoModulo': '', 'asignado': false }",
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
def get_user_modules(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_user_modules(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['resultado']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene modulos asignados"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene modulos asignados"})  



#funcion para determianr los datos laborales usuario 
@user_router.get ('/user/{id}/datos_laborales',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def get_user_datos_laborales(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_datos_laborales_userid(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos laborales"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos laborales"})  


#funcion para determinar los datos de pago usuario 
@user_router.get ('/user/{id}/datos_pago',
tags=['Usuarios'],
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
                                    "data": "{'id':'1','user_id':'1','medio':'1','banco_id':'1','tipo_cuenta': '1','numero_cuenta':'123456','created':'2024-03-14T08:59:43','updated':'2024-03-14T09:01:45','creator_user':'1','updater_user':'1'}",
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
def get_datos_pago_userid(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_datos_pago_userid(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos laborales"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos laborales"}) 


#funcion para determinar los datos de colacion usuario 
@user_router.get ('/user/{id}/colacion',
tags=['Usuarios'],
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
                                    "data": "{'id':'1','user_id':'1','medio':'1','banco_id':'1','tipo_cuenta': '1','numero_cuenta':'123456','created':'2024-03-14T08:59:43','updated':'2024-03-14T09:01:45','creator_user':'1','updater_user':'1'}",
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
def get_datos_colacion(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_datos_colacion(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        elif (result["result"]=="-2"):
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos de colacion"})     
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene datos laborales"}) 


#funcion para determianr a que grupo pertenece el  usuario 
@user_router.get ('/user/{id}/grupo',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
                "description": "Grupo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo Encontrado",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def get_user_grupo(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado del grupo 
    result = userController(db).get_user_group(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene grupo asignado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene modulos asignados"})  


#funcion para determianr si un usuario tiene o no su foto en el sistema
@user_router.get ('/user/{id}/have_pic',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
                "description": "Tiene Foto",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tiene Foto",
                                    "data": "{'estado': '1'}",
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
                "description": "No Tiene Foto",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"No Tiene Foto",
                                    "data": "{'estado': '0'}",
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
def get_user_have_pic(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado del grupo 
    result = userController(db).get_user_have_pic(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            return JSONResponse(status_code=200,content={"message":"Este usuario tiene foto","data":"1"})    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene foto","data":"0"})
    
    
    return JSONResponse(status_code=520,content={"message":"Ocurrio un error que no pudo ser controlado"})  


#funcion para determianr si un usuario tiene o no su foto en el sistema
@user_router.get ('/user/{id}/profile',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
                "description": "Perfil del Usuario",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Perfil del Usuario",
                                    "data": "{'id': '1','sexo_id': '1','updated': '1990-01-01T00:00:00','direccion': 'Av. Parque Viña Santa Blanca 0411 dpto. 303','departamento_id': '1','en_uso': '1','rut': '1','estado_civil_id': '1','creator_user': '1','nomregion': 'Lib. Gral. B. OHiggins','nomdepartamento': 'Administración','terceros': '0','rut_provisorio': '','nacionalidad_id': '1','updater_user': '1','grupo_empleados_id': '1','nombre_sede': 'SEDE UNO','rut_tercero': '','Nacionalidad': 'CHILENA','username': 'root','email': 'example@micorreo.com','orden': '8','nombre_grupo': 'Administrativo','nombre_tercero': '','nombres': 'Admin','password': '$2b$12$r/z4etm/Z1izSDLkb9swku2FbOljYJ94gHBKMLjL4B/RaNTdMJIZi','fijo': '226656168','nomcomuna': 'Rancagua','sueldo': '143088.0000','email_tercero': 'No Asignado','apellido_paterno': 'Root','activo': '1','movil': '939024766','sociedad_id': '1','cargo': 'CARGO DEMO','vacaciones_acumuladas': '0','apellido_materno': '','created': '1990-01-01T00:00:00','region_id': '6','sede_id': '1','banco_id': '1','fecha_nacimiento': '1990-01-01','comuna_id': 610'1','numero_cuenta': '12345678'}",
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
                "description": "No Tiene Foto",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"No Tiene Foto",
                                    "data": "{'estado': '0'}",
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
def get_user_profile(id:int = Path(ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    # almacenamos el listado del grupo 
    result = userController(db).get_user_profile(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"message":"Pefil Encontrado","data":jsonable_encoder(data)})    
        elif(result["result"]=="-2"):
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene perfil"})
        else:
            cadena=result['cadenaError']
            return JSONResponse(status_code=520,content={"message":f"Error {cadena}"})
    
    return JSONResponse(status_code=520,content={"message":"Ocurrio un error que no pudo ser controlado"})  



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
def update_user(usuario:User, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')),id : int =Path(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = userController(db).update_user(user_updater,usuario,id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado","Usuario":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    elif (result['result']=="-2"):
        return JSONResponse(status_code=521,content={"message":f"Este Username esta siendo usado por otro usuario, userId={result['UserId']}, por favor rectifique los datos"})     
    elif (result['result']=="-4"):
        return JSONResponse(status_code=522,content={"message":f"Este RUT está registrado a nombre de otro usuario, userId={result['UserId']}, por favor rectifique los datos"})       
    elif (result['result']=="-5"):
        return JSONResponse(status_code=522,content={"message":f"Este RUT  provisorio está registrado a nombre de otro usuario, userId={result['UserId']}, por favor rectifique los datos"})       
    elif (result['result']=="-6"):
        cadenaError=result['cadenaError']
        return JSONResponse (status_code=523,content={"message":cadenaError})      
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})         


# Función para actualizar  los datos personales un usuario
@user_router.put ('/user/{id}/update_datos_personales',
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
def update_user_datos_personales(usuario:DatosPersonalesSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')),id : int =Path(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = userController(db).update_user_datos_personales(user_updater,usuario,id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado","Usuario":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    elif (result['result']=="-4"):
        return JSONResponse(status_code=522,content={"message":f"Este RUT está registrado a nombre de otro usuario, userId={result['UserId']}, por favor rectifique los datos"})       
    elif (result['result']=="-6"):
        cadenaError=result['cadenaError']
        return JSONResponse (status_code=523,content={"message":cadenaError})      
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})         



# Función para actualizar  los datos de contacto y ubicacion
@user_router.put ('/user/{id}/update_datos_contacto_ubicacion',
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
def update_user_datos_contacto_ubicacion(contactoUbicacion:ContactUbicationUserSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')),id : int =Path(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = userController(db).update_user_datos_contacto_ubicacion(user_updater,contactoUbicacion,id) 
    if (result['result']=="1"):
        return JSONResponse(status_code=201,content={"message":"Datos actualizados"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Datos no encontrados"}) 
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})         


# Función para actualizar  el grup al cual pertenece el usuario
@user_router.put ('/user/{id}/update_user_group',
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
def update_user_group(idgroup : int, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')),id : int =Path(ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = userController(db).update_user_group(user_updater,idgroup,id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Usuario asignado a un nuevo grupo","Usuario":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    elif (result['result']=="-6"):
        cadenaError=result['cadenaError']
        return JSONResponse (status_code=523,content={"message":cadenaError})      
    else:
        codigo=result['result']
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {codigo} {cadenaError} "})         

# Función para actualizar  los datos personales un preuser
@user_router.put ('/user/{id}/update_preuser',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
            "description": "Usuario Actualizado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Usuario Actualizado"
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
            "description": "Error en los formatos de los datos",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Error en los formatos de los datos",
                            "estado":"System Error"
                        }
                    } 
                }       
            },                                   

    }
)
def update_preuser2(preUser:PreUserSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')),id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS')))->dict:
    db = Session()
    # buscamos el registro
    result = userController(db).update_preuser2(id,user_updater,preUser) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario actualizado"})    
    elif (result['result']=="-2"):
        cadenaErrores=result["estado"]
        return JSONResponse (status_code=521,content={"message":"Error en los formatos de los datos","estado":cadenaErrores})        
    elif (result['result']=="-1"):
        data=result['user']
        return JSONResponse(status_code=520,content={"message":f"Este Documento está registrado a nombre de otro usuario ","user":jsonable_encoder(data)})       
    elif (result['result']=="-3"):
        return JSONResponse(status_code=404,content={"message":f"Este Usuario no existe, Id del Usuario:{id }"})       

    else:
        return JSONResponse(status_code=500,content={"message":f"Ocurrió un error que no pudo ser controlado {result['result']}"})              


# Funcion para crear los datos personles de un usuario
@user_router.put ('/user/{id}/save_preuser',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        200: {
            "description": "Data Actualizada",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el preregistro del usuario en el sistema",
                        }
                    } 
                }       
            },
        201: {
            "description": "Se creo el preregistro del usuario en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo el preregistro del usuario en el sistema",
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
            "description": "Ocurrió un error que no pudo ser controlado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Cadena de error",
                            "estado":"System Error"
                        }
                    } 
                }       
            }, 

    }
)
def save_preuser(preregistro_user2:PreUser2Schema, id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")), userUpdater : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=userController(db).update_pre_user(preregistro_user2,id,userUpdater)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newUserId=result["newUserId"]
        return JSONResponse (status_code=201,content={"message":"Se creo el usuario en el sistema","newUserId":newUserId})  
    if (estado=="2") :
        # se inserto el registro sin problemas
        return JSONResponse (status_code=200,content={"message":"Datos Actualizados"})         
    elif (estado=="-2"):
        userExist=jsonable_encoder(result['user'])
        return JSONResponse (status_code=422,content={"message":"Este RUT ya fue registrado en el sistema, no puede volver a insertarlo","User":userExist})     
    elif (estado=="-1"):
        cadenaError=result['cadenaError']
        return JSONResponse (status_code=521,content={"message":cadenaError})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})

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
def activate_user( user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).activate_user(user_updater,id) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario activado"})    
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
def deactivate_user(user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).deactivate_user(user_updater,id) 
    if (result['result']=="1"):
        return JSONResponse(status_code=200,content={"message":"Usuario desactivado"})    
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
def update_password_user( password:str = Query (min_length=os.getenv("MIN_LENGTH_USER_PASSWORD"), max_length=os.getenv("MAX_LENGTH_USER_PASSWORD")) ,id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS')), user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).update_password_user(id,user_updater, password) 
    if (result['result']=="1"):
        newPassword=result["newPassword"]
        return JSONResponse(status_code=200,content={"message":f"Password de Usuario Actualizado"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  
    




# Función para actualizar  los datos de salario de un usuario en el apartado de perfil
@user_router.put ('/user/{id}/update_datos_laborales_salario',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Datos Actualizados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Datos Laborales actualizados"
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
def update_datos_laborales_salario(laboralesA : DatosLaboralesSalarioSchema, id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS')), user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).update_laborales_salario(id,user_updater, laboralesA) 
    if (result['result']=="1"):
        return JSONResponse(status_code=201,content={"message":"Datos Laborales actualizados"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"No existen datos laborales de este usuario"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})  
    

# Función para actualizar  los datos de contrato de un usuario en el apartado de perfil
@user_router.put ('/user/{id}/update_datos_laborales_contrato',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Datos Actualizados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Datos Laborales actualizados"
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
def update_datos_laborales_contrato(laboralesA : DatosLaboralesContratoSchema, id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS')), user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).update_laborales_contrato(id,user_updater, laboralesA) 
    if (result['result']=="1"):
        return JSONResponse(status_code=201,content={"message":"Datos Laborales actualizados"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"No existen datos laborales de este usuario"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})  



# Función para actualizar  los datos de contrato de un usuario en el apartado de perfil
@user_router.put ('/user/{id}/update_datos_laborales_puesto',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        201: {
            "description": "Datos Actualizados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Datos Laborales actualizados"
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
def update_datos_laborales_puesto(laboralesA : DatosLaboralesPuestoSchema, id : int = Path (ge=1, le=os.getenv('MAX_ID_USERS')), user_updater: int = Query (ge=1, le=os.getenv('MAX_ID_USERS'))):
    db = Session()
    # buscamos el registro
    result = userController(db).update_laborales_puesto(id,user_updater, laboralesA) 
    if (result['result']=="1"):
        return JSONResponse(status_code=201,content={"message":"Datos Laborales actualizados"})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"No existen datos laborales de este usuario"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})  



'''
============================ rutas DELETE =================================================================
'''
# Funcion para eliminar CV del profile de un usuario
@user_router.delete ('/user/{id}/delete_prospecto',
tags=['Usuarios'],
dependencies=[Depends(JWTBearer())], 
responses=
    { 
        202: {
            "description": "Se elimino al prospecto del sistema",
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
        404: {
            "description": "Prospecto no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Prospecto no encontrado"
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
            "description": "No se pudo eliminar por que tiene registro en las tablas de liquidaciones",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"No se pudo eliminar por que tiene registro en las tablas de liquidaciones",
                            "estado":"System Error"
                        }
                    } 
                }       
            },                       
    })
def delete_prospecto(id : int = Path (ge=1, le=os.getenv("MAX_ID_USERS")),creatorUserId: int = Query(ge=1, le=os.getenv("MAX_ID_USERS"))):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).delete_prospecto(id,creatorUserId)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['estado']
            return JSONResponse(status_code=202,content=jsonable_encoder(data))    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"Prospecto no encontrado"})     
        elif (result["result"]=="-2"):
            # no se puede eliminar porque tiene registros en las tablas de liquidaciones
            return JSONResponse(status_code=521,content={"message":"No se pudo eliminar por que tiene registro en las tablas de liquidaciones"})    
    
    return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})  

'''
============================ rutas faltantes =================================================================
'''
'''
	asignate_user_department        post
	asignate_user_payments          post
	asignate_masive_user_groups     post 
	asignate_masive_user_groups     post   
	asignate_user_branch            post        

	updater_payments                put
	update_user_branch              put
    update_user_department          put

'''