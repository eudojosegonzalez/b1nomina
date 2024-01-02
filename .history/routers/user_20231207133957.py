from fastapi import APIRouter,Body,Path
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from datetime import date


# esta variable define al router
user_router = APIRouter()


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



# Crear el Usuario
@user_router.post ('/create_users', tags=["Usuarios"])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@user_router.get ('/users', tags=["Usuarios"])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@user_router.get ('/users/{id}', tags=["Usuarios"])
def get_user(id: int = Path (title="ID del usuario que se desea consultar",gt=1, le=2000)):
    return f"Ver el usuario {id}"


# Actualizar el usuario representado por el ID
@user_router.put ('/users/{id}/update', tags=["Usuarios"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"
        
