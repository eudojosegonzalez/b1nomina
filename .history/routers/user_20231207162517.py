from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from utils.jwt_managr import create_token,validate_token
#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token


#from config.database import engine, Base
from schemas.user import User


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
user_router = APIRouter()

# metodo que logea compara el email y la clave enviadas desde  el formulario
# se crea el token si la claeve y el usuario coinciden
@user_router.post("/login", tags=["auth"])
def login(user: User):
    if (user.email=="eudo@gmail.com") and (user.password=='12345'):
        token: str = create_token(user.dict())
        return JSONResponse (status_code=202,content={"token":token})
    
    return JSONResponse (status_code=401,content={"message":"No autorizado"})    

@user_router.post("/validate", tags=["auth"])
def validate(token : str = Body):
    if (validate_token(token)):
        return JSONResponse (status_code=201,content={"message":"autorizado"})   
    else:
        return JSONResponse (status_code=401,content={"message":"mo autorizado"})
    

#Funcion para crear un usuario
@user_router.post ('/create_user',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def create_user():
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

