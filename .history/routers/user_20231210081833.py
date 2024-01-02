from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
from datetime import date,datetime


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
user_router = APIRouter()

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
                ExpTokenTime=datetime.datetime.now() + datetime.timedelta(minutes=30)
                # creamos un diccionario para generar el token del usuario
                userDict={"username":username,"password":password,"exp":ExpTokenTime}
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
    

#Funcion para crear un usuario
@user_router.post ('/create_user',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def create_user(usuario:User)->dict:
    db = Session()
    new_usuario = UsuarioModel(
        rut=usuario.rut,
        rut_provisorio=usuario.rut_provisorio,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        fecha_nacimiento=usuario.fecha_nacimiento,
        sexo_id=usuario.sexo_id,
        estado_civil_id=usuario.estado_civil_id,
        nacionalidad_id=usuario.nacionalidad_id,
        username=usuario.username,
        password=hash_password(usuario.password),
        activo=usuario.activo,
        created=datetime.datetime.now(),
        update=datetime.datetime.now(),
        creator_user="0",
        update_user_user="0"
    )
    db.add(new_usuario)
    db.commit()

    return JSONResponse (status_code=201,content={"message":"Usuario Creado"})     


#Funcion para consultar los usuarios del sistema
@user_router.get ('/list_users',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def list_user()->list[User]:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = userController(db).get_users()
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})            
        


#Funcion para consultar un usuario
@user_router.get ('/user/{id}',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user():
    return JSONResponse (status_code=200,content={"message":"Obtener un Usuario por ID"})  



#Funcion para actualizar un usuario
@user_router.put ('/user/{id}/update',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def update_user():
    return JSONResponse (status_code=200,content={"message":"Actualizar un usuario por ID"})  

