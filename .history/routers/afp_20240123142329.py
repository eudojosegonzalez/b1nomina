from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from config.database import engine, Base
#from schemas.user import Bancos

#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objketos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token


# importamos el controlador 
from controller.afp import AFPController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
afp_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@afp_router.post ('/create_afp', 
tags=["Instituciones AFP"],status_code=200, 
#dependencies=[Depends(JWTBearer())],
)
def create_afp():
    return JSONResponse (status_code=201,content={"message":"Se creo una institución AFP en el sistema"})  

# ruta para listar las Instituciones AFP 
@afp_router.get ('/list_afp', 
tags=["Instituciones AFP"],
status_code=200, 
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        403: {
            "description": "Forbiden",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Not authenticated"
                        }
                    } 
                }       
            },             
        500: {
            "description": "Su session ha expirado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Su session ha expirado",
                            "estado":"Signature has expired"
                        }
                    } 
                }       
            },                         
        520: {
            "description": "Ocurrió un error que no pudo ser controlado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Ocurrió un error que no pudo ser controlado",
                            "estado":"System Error"
                        }
                    } 
                }       
            },                       
    }
)
def list_afp(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = AFPController(db).list_AFP(page,records)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})     

# ruta para consultar una Institución AFP por Id
@afp_router.get ('/afp/{id}', 
tags=["Instituciones AFP"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "AFP encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"AFP encontrado",
                                    "data": "{'id':1,'codigo_previred' : '001','nombre'  : 'AFP Prueba','cotizacion' : 0,'cuenta_AFP' : '0001' ,'sis' : 0,'cuenta_sis_cred' : '','cuenta_ahorro_AFP_cuenta2' : '','codigo_direccion_trabajo': '','user_creator':1, 'user_updater':1,'created':'1990-01-01 01:00','updated':'1990-01-01 01:00' }",
                                }
                        } 
                    
                } 
            },         
        403: {
            "description": "Forbiden",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Not authenticated"
                        }
                    } 
                }       
            },  
        404: {
            "description": "AFP no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Banco no encontrado"
                        }
                    } 
                }       
            },   
        500: {
            "description": "Su session ha expirado",
            "content": { 
                "application/json":
                    { "example":
                        {
                            "message":"Su session ha expirado",
                            "estado":"Signature has expired"
                        }
                    } 
                }       
            },                                                           
    }   
)
def get_afp(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = AFPController(db).get_AFP(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"AFP":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"AFP no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Banco no encontrado"}) 

# ruta para actualizar una institución AFP por Id
@afp_router.put ('/afp/{id}/update', 
tags=["Instituciones AFP"],
status_code=200, 
dependencies=[Depends(JWTBearer())]
)
def update_afp(id: int):
    return JSONResponse (status_code=200,content={"message":"Actualizar una Institución AFP por ID"})      
