from fastapi import FastAPI,Depends, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

'''from pydantic import BaseModel,Field'''

'''from utils.jwt_managr import create_token,validate_token'''
from config.database import engine, Base
#importamos el routers
#from routers.movie import movie_router
from routers.user import user_router
from routers.contacto import user_contact_router
from routers.localizacion import user_localization_router
from routers.bancos import bancos_router
from routers.afp import afp_router
from routers.basic_parameter import basic_parameter_router

from middleware.error_handler import ErrorHandler

#descripcion de los endpoints
tags_metadata = [
    {
        "name": "Auth",
        "description": "Operaciones de validación de usuario y generación de tokens",
    },
    {
        "name": "Usuarios",
        "description": "Operaciones relacionadas con los datos personales de los usuarios",
    },
    {
        "name": "Contacto",
        "description": "Operaciones relacionadas con los datos de contacto de los usuarios",
    },    
    {
        "name": "Localizacion",
        "description": "Operaciones relacionadas con los datos de localizacion de los usuarios",
    },     
    {
        "name": "Instituciones AFP",
        "description": "Operaciones relacionadas con las instituciones AFP",
    },    
    {
        "name": "Bancos",
        "description": "Operaciones relacionadas con las instituciones Bancarias",
    },
    {
        "name": "Bancos",
        "description": "Operaciones relacionadas con los Parámetros Básicos del Sistema",
    },          
]


app = FastAPI(openapi_tags=tags_metadata)
app.title='Core B1 Nomina by Kyros'
app.version='V1.0'


# manejador de errores
app.add_middleware(ErrorHandler)

#inclusión de los endpoints
app.include_router(user_router)
app.include_router(user_contact_router)
app.include_router(user_localization_router)
app.include_router(afp_router)
app.include_router(bancos_router)
app.include_router(basic_parameter_router)
#app.include_router(movie_router)

# esto crea la base de datos si no existe al empezar la app
Base.metadata.create_all(bind=engine)


@app.get('/',tags=['Home'])
def home():
    return RedirectResponse("/docs")
    '''return HTMLResponse("<h4>Core B1 Nomina by Kyros</h4>")'''


