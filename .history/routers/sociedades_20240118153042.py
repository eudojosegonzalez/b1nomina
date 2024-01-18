'''
Rutas de Sociedades
2024-01
'''
import os

#importamos la libreria para cargar los archivos de entorno
import dotenv

from fastapi import APIRouter,Body
from fastapi import Path,Query, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
#from utils.jwt_managr import create_token,validate_token
from config.database import engine, Base

#from typing import  Optional, List
from typing import  List
from config.database import Session
# dependencia que coinvierte los objetos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token

#importamos el banco
from schemas.sociedades import Sociedades as SocidadeSchema

# importamos el controlador 
from controller.sociedades import sociedadesController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
sociedades_router = APIRouter(prefix="/V1.0")

# -------- Rutas Bancos ------------
# ruta para crear las Sociedades
@sociedades_router.post ('/create_sociedad', 
tags=["Sociedades"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Banco en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Banco en el sistema",
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
def create_sociedad(sociedad:SocidadeSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=sociedadesController(db).create_sociedad(sociedad,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newSociedad=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo una sociedad en el sistema","Sociedad":jsonable_encoder(newSociedad)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe una sociedad con este nombre, no puede volver a crearla","Sociedad":jsonable_encoder(result['data'])})     
    elif (estado=="-2"):
        return JSONResponse (status_code=521,content={"message":"existe una sociedad con este rut, no puede volver a crearla","Sociedad":jsonable_encoder(result['data'])})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar las sociedades en el sistema
@sociedades_router.get ('/list_sociedad', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
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
def list_sociedad(page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_sociedades(page,records)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para consultar una sociedad por Id
@sociedades_router.get ('/sociedad/{id}', 
tags=["Sociedades"],
#dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Banco encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Banco encontrado",
                                    "data": "{'id':'1','rut': '12345678912','rut': '12345678912', 'nombres': 'Pedro ', 'apellido_paterno': 'Perez', 'apellido_materno': 'Martinez', 'fecha_nacimiento': '1990-01-01','sexo_id': '1', 'estado_civil_id': '1', 'nacionalidad_id': '1','username': 'pperez' 'password': '12345678','activo':'1','created':'1990-01-01 10:00','updated':'1990-01-01 11:00','creator_user':'1','updater_user':'1' }",
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
            "description": "Banco no encontrado",
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
def get_sociedad(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_sociedad(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Banco":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Banco no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"})      



# ruta para listar los datos historicos de la sociedades por ID
@sociedades_router.get ('/sociedad/{id}/list_historico_sociedad', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
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
def list_history_sociedad(page : int = 1, records : int = 20, id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_history_sociedades(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sociedad por nombre o rut
@sociedades_router.get ('/search_sociedad', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Bancos encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sociedad encontrada",
                                    "data": "{'rut': 'RutDemo','nombre':'Demo','direccion': 'Direccion Demo','region_id': 1,'comuna_id': 1,'ciudad':'Demo ciudad','icono':'','created':'1990-01-01 10:52','updatedted':'1990-01-01 10:52','user_creator':1,'user_updater':1}",
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
def search_sociedad(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")), page : int = 1, records : int = 20)->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).search_sociedades(finding,page,records)
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


# ruta para actualizar una sociedad por Id
@sociedades_router.put ('/sociedad/{id}/update', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
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
def update_sociedad(sociedad:SocidadeSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = sociedadesController(db).update_sociedad(sociedad, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Sociedad actualizada","Sociedad":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
