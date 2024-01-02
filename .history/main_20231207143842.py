from fastapi import FastAPI
from fastapi import   Request, HTTPException
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
app.include_router(user_router)
app.include_router(basic_parameter_router)
app.include_router(afp_router)
app.include_router(bancos_router)



@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h4>B1 Nomina by Kyros</h4>")
    


