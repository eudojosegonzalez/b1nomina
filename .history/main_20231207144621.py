from fastapi import FastAPI
from fastapi import   Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field
from utils.jwt_managr import create_token,validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


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
@user_router.post ('/create_users', tags=["Usuarios"],status_code=201,dependencies=[Depends(JWTBearer)])
def create_user():
    return "Hello word!"


# Listar todos los usuarios del sistema
@user_router.get ('/users', tags=["Usuarios"],status_code=201,dependencies=[Depends(JWTBearer)])
def list_users():
    return "Hello word!"


# Listar ver el representado por el ID
@user_router.get ('/users/{id}', tags=["Usuarios"])
def get_user(id: int = Path (title="ID del usuario que se desea consultar",ge=1, le=2000)):
    return f"Ver el usuario {id}"


# Actualizar el usuario representado por el ID
@user_router.put ('/users/{id}/update', tags=["Usuarios"])
def update_user(id: int):
    return f"Actualizar el usuario! {id}"