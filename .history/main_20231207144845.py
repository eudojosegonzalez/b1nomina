from fastapi import FastAPI
from fastapi import   Request, HTTPException, Depends
from fastapi import   Body,Path, Query, Depends,Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field
from utils.jwt_managr import create_token,validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import date


# importamos los routers
from routers.user import user_router
from routers.basic_parameter import basic_parameter_router
from routers.afp import afp_router
from routers.bancos import bancos_router


# creamos la Instancia de FastAPI
app = FastAPI()


# Nombre de la Aplicacion
app.title="Core B1 Nómina by Kyros"
# Versión de la Aplicacion
app.version="1.0"

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
@app.post("/login", tags=["auth"])
def login(credenciales: Credentials):
    if (credenciales.username=="egonzalez") and (credenciales.password=='12345678'):
        token: str = create_token(credenciales.dict())
        return JSONResponse (status_code=202,content={"token":token})
    
    return JSONResponse (status_code=401,content={"message":"No autorizado"})    


@app.post("/validate", tags=["auth"])
def validate(token : str = Body):
    if (validate_token(token)):
        return JSONResponse (status_code=201,content={"message":"autorizado"})   
    else:
        return JSONResponse (status_code=401,content={"message":"mo autorizado"})   
        
        

# instanciamos las rutas
app.include_router(basic_parameter_router)
app.include_router(afp_router)
app.include_router(bancos_router)



@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h4>B1 Nomina by Kyros</h4>")
    



# Crear el Usuario
@app.post ('/create_users', tags=["Usuarios"],status_code=201,dependencies=[Depends(JWTBearer)])
def create_user():
    return "Hello word!"



# Crear el Usuario
@app.post ('/create_users', tags=["Usuarios"],status_code=201,dependencies=[Depends(JWTBearer)])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@user_router.get ('/users', tags=["Usuarios"],status_code=201,dependencies=[Depends(JWTBearer)])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@app.get ('/users/{id}', tags=["Usuarios"])
def get_user(id: int = Path (title="ID del usuario que se desea consultar",ge=1, le=2000)):
    return f"Ver el usuario {id}"


# Actualizar el usuario representado por el ID
@app.put ('/users/{id}/update', tags=["Usuarios"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"