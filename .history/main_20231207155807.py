from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field

from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base
#importamos el routers
from routers.movie import movie_router
from routers.user import user_router
from routers.bancos import bancos_router
from routers.afp import afp_router

from middleware.error_handler import ErrorHandler

movies=[
    {'id':1,
     'title':'Avatar',
     'overview':'En un lejano planeta',
     'year':2009,
     'rating':'7.8',
    'category':'Accion'
     },
    {'id':2,
     'title':'Avatar 2',
     'overview':'El camino del Agua',
     'year':2022,
     'rating':'9',
    'category':'Suspenso'
     }     
]

app = FastAPI()
app.title='Core B1 Nomina by Kyros'
app.version='1.0.0'
# manejador de errores
app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(afp_router)
app.include_router(bancos_router)
app.include_router(movie_router)


Base.metadata.create_all(bind=engine)

@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h4>Hola</h4>")


