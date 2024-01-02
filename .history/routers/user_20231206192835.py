from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
'''from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
from schemas.user import User'''

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
        
# Ruta de inicio
@app.get ('/login', tags=["Home"])
def login():
    return HTMLResponse('Login', status_code=200)

# Crear el Usuario
@app.post ('/create_users', tags=["Usuarios"])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@app.get ('/users', tags=["Usuarios"])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@app.get ('/users/{id}', tags=["Usuarios"])
def get_user(id: int):
    return f"Ver el usuario {id}"


# Actualizar el usuario representado por el ID
@app.put ('/users/{id}/update', tags=["Usuarios"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"
        
