from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
from schemas.user import User

from fastapi import APIRouter
from fastapi import Path,Query, Depends
from fastapi.responses import  JSONResponse
#from pydantic import BaseModel,Field
#from typing import  Optional, List
from typing import  List
from config.database import Session
from models.movie import Movie as MovieModel
# dependencia que coinvierte los objketos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token


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
    


@user_router.post ('/create_user',tags=['Usuarios'],status_code=200, dependencies=[Depends(JWTBearer())])
def create_user():
    return JSONResponse (status_code=201,content={"message":"Usuario Creado"})            
