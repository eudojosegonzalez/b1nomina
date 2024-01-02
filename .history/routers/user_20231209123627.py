from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from utils.jwt_managr import create_token,validate_token
#from typing import  Optional, List
from typing import  List
# importamos desde la configuracion de la Base de datos las clases
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token
from utils.hasher import hash_password,verify_password

from datetime import date,datetime


# esto importa la tabla desde la definicione de modelos
from models.user import Usuario as UsuarioModel
#importamos el la tabla
from schemas.user import User


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

# la configuracion de la base de datos
from config.database import Session


# esta variable define al router
user_router = APIRouter()

# metodo que logea compara el email y la clave enviadas desde  el formulario
# se crea el token si la claeve y el usuario coinciden
@user_router.post("/login", tags=["Auth"])
def login(username : str = Body, password : str = Body):
    session = Session()
    passWord=hash_password(password)
    
    userVerified = session.query(UsuarioModel).filter(UsuarioModel.username == username,UsuarioModel.password==password).first()

    if (userVerified):
        userDict={"username":username,"password":password}
        token: str = create_token(userDict)
        return JSONResponse (status_code=202,content={"token":token})
    
    return JSONResponse (status_code=401,content={"message":f"No autorizado {passWord}"})    


@user_router.post("/validate", tags=["Auth"])
def validate(token : str = Body):
    if (validate_token(token)):
        return JSONResponse (status_code=201,content={"message":"autorizado"})   
    else:
        return JSONResponse (status_code=401,content={"message":"mo autorizado"})
    

#Funcion para crear un usuario
@user_router.post ('/create_user',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def create_user(usuario:User)->dict:
    db = Session
    '''    
    id : int = Field (ge=1, lt= 2000)
    rut: str = Field (min_length=8, max_length=100)
    rut_provisorio : Optional[str]  = Field (min_length=8, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    apellido_materno : str = Field (min_length=2, max_length=100)
    fecha_nacimiento : date
    sexo_id : int  = Field (ge=1, le= 2)
    estado_civil_id : int  = Field (ge=1, le= 5)
    nacionalidad_id : int   = Field (ge=1, le= 200)
    username : str  = Field (min_length=5, max_length=200)   
    password : str = Field (min_length=8, max_length=200)
    activo : bool 
    created : datetime
    updated : datetime
    creator_user : int = Field (ge=1, lt= 2000)
    updateter_user : int = Field (ge=1, lt= 2000) 
    '''
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
def list_user():
    return JSONResponse (status_code=200,content={"message":"Listado de Usuarios"})           


#Funcion para consultar un usuario
@user_router.get ('/user/{id}',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def get_user():
    return JSONResponse (status_code=200,content={"message":"Obtener un Usuario por ID"})  



#Funcion para actualizar un usuario
@user_router.put ('/user/{id}/update',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def update_user():
    return JSONResponse (status_code=200,content={"message":"Actualizar un usuario por ID"})  

