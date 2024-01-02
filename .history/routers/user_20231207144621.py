from typing import Any, Coroutine, Optional
from fastapi import APIRouter,Body,Path, Query, Depends,Request, HTTPException
from utils.jwt_managr import create_token,validate_token
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from datetime import date
from starlette.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer



# esta variable define al router
user_router = APIRouter()

#clase para validar el,token en las rutas
class JWTBearer (HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data = validate_token (auth.credentials) 
        if (data['username']!= "egonzalez"):
            raise HTTPException (status_code=403,detail="Credenciales erradas") 


#Clase usuario para efectos de práctica
class User(BaseModel):
    id : int = Field (title='ID del usuario', gt=0,le=100),
    rut : str = Field(title='RUT del usuario', min_length=10, max_length=100),
    rut_provisorio : str = Field(title='RUT del usuario', min_length=10, max_length=100),
    nombres : str = Field(title='RUT del usuario', min_length=3, max_length=100),
    apellido_paterno  : str = Field(title='RUT del usuario', min_length=3, max_length=100),
    apellido_materno  : str = Field(title='RUT del usuario', min_length=3, max_length=100),
    fecha_nacimiento  : date = Field(title='Fecha de Nacimiento del usuario'),
    sexo_id : int = Field (title='Sexo del usuario', ge=1,le=2),
    estado_civil_id: int = Field (title='Sexo del usuario', ge=1,le=5),    
    nacionalidad_id : int = Field (title='Sexo del usuario', ge=1,le=200),
    username  : str = Field(title='RUT del usuario', min_length=8, max_length=250),
    password  : str = Field(title='RUT del usuario', min_length=10, max_length=250)


#clase para recibir las credenciales y contrastar contra el usuario
class Credentials(BaseModel):
    username  : str = Field(title='Nombre de usuario', min_length=8, max_length=250),
    password  : str = Field(title='Contraseña', min_length=8, max_length=250)



# metodo que logea compara el username y la clave enviadas desde  el formulario
# se crea el token si la claeve y el usuario coinciden
@user_router.post("/login", tags=["auth"])
def login(credenciales: Credentials):
    if (credenciales.username=="egonzalez") and (credenciales.password=='12345678'):
        token: str = create_token(credenciales.dict())
        return JSONResponse (status_code=202,content={"token":token})
    
    return JSONResponse (status_code=401,content={"message":"No autorizado"})    


@user_router.post("/validate", tags=["auth"])
def validate(token : str = Body):
    if (validate_token(token)):
        return JSONResponse (status_code=201,content={"message":"autorizado"})   
    else:
        return JSONResponse (status_code=401,content={"message":"mo autorizado"})


        
