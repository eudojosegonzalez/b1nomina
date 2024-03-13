'''
Rutas de Instituciones APV
2024-01
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv

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

#importamos el schema de datos del AFP
from schemas.apv import  APVInstituciones as APVSchema

# importamos el controlador 
from controller.apv import APVController

#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
apv_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@apv_router.post ('/create_apv', 
tags=["Instituciones APV"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo una institucion AFP en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo una institucion AFP en el sistema",
                            "newUserId":"1"
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
def create_apv(apv:APVSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=APVController(db).create_apv(afp,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newAFP=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una institucion AFP en el sistema","Banco":jsonable_encoder(newAFP)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una AFP con este nombre, no puede volver a crearlo","AFP":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una AFP con este codigo, no puede volver a crearlo","AFP":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})   

# ruta para listar las Instituciones AFP 
@apv_router.get ('/list_apv', 
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
def list_apv(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = APVController(db).list_apv(page,records)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})     



# ruta para listarlos datos historicos de la institucion AFP 
@apv_router.get ('/afp/{id}/list_historico_apv', 
tags=["Instituciones AFP"],
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
def list_history_apv(page : int = 1, records : int = 20, id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = APVController(db).list_history_apvs(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para consultar una Institución AFP por Id
@apv_router.get ('/afp/{id}', 
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
                                    "data": "{'id':1,'codigo_previred' : '001','nombre'  : 'AFP Prueba','cotizacion' : 0,'cuenta_apv' : '0001' ,'sis' : 0,'cuenta_sis_cred' : '','cuenta_ahorro_apv_cuenta2' : '','codigo_direccion_trabajo': '','user_creator':1, 'user_updater':1,'created':'1990-01-01 01:00','updated':'1990-01-01 01:00' }",
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
def get_apv(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = APVController(db).get_apv(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"AFP":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"AFP no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Banco no encontrado"}) 


# ruta para buscar un banco por nombre o codigo
@apv_router.get ('/search_apv', 
tags=["Instituciones AFP"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "AFPs encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"AFPs encontrado",
                                    "data": "{'id':1,'codigo_previred' : '001','nombre'  : 'AFP Prueba','cotizacion' : 0,'cuenta_apv' : '0001' ,'sis' : 0,'cuenta_sis_cred' : '','cuenta_ahorro_apv_cuenta2' : '','codigo_direccion_trabajo': '','user_creator':1, 'user_updater':1,'created':'1990-01-01 01:00','updated':'1990-01-01 01:00' }",
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
            "description": "La búsqueda no arrojó resultados",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"La búsqueda no arrojó resultados"
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
def search_apv(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")), page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = APVController(db).search_apv(finding,page,records)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"La búsqueda no arrojó resultados"})    
        else:
            return JSONResponse(status_code=520,content={"message":"System Error","error":result})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})
    

# ruta para actualizar una institución AFP por Id
@apv_router.put ('/afp/{id}/update', 
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
def update_apv(apv: APVSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = APVController(db).update_apv( apv, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"AFP actualizado","AFP":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"AFP no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})    
