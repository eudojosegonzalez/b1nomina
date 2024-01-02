from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field


# importamos los routers
from routers.user import user_router
from routers.basic_parameter import basic_parameter_router
from routers.afp import afp_router
from routers.bancos import bancos_router


# creamos la Instancia de FastAPI
app = FastAPI()


# Nombre de la Aplicacion
app.title="B1 Nómina by Kyros"
# Versión de la Aplicacion
app.version="1.0"



# instanciamos las rutas
app.include_router(user_router)
app.include_router(basic_parameter_router)
app.include_router(afp_router)
app.include_router(bancos_router)



@app.get('/',tags=['home'])
def message():
    return HTMLResponse("<h4>B1 Nomina by Kyros</h4>")
    


