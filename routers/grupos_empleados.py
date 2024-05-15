'''
Rutas de Grupos Empleados
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

#importamos el Sede
from schemas.grupos_empleados import GruposEmpleado as GruposEmpleadoSchema

# importamos el controlador 
from controller.grupos_empleados import GrupoEmpleadosController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
grupos_empleados_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear las Sociedades
@grupos_empleados_router.post ('/create_grupo_empleado', 
tags=["Grupos Empleados"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Grupo de Empleados en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Grupo de Empleados en el sistema",
                            "newGrupoEmpleado":"1"
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
def create_grupo_empleados(grupoEmpleado:GruposEmpleadoSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=GrupoEmpleadosController(db).create_grupo_empleados(grupoEmpleado,userCreatorId)
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
             


# ruta para consultar una sociedad por Id
@grupos_empleados_router.get ('/grupo_empleados/{id}', 
tags=["Grupos Empleados"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupo de Empleados encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Empleados",
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'Administrativo','updated': '2024-02-05T10:00:00','updater_user': '1','es_honorario': '0','created': '2024-02-05T10:00:00','creator_user': '1'}"
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
            "description": "Sede no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Sede no encontrado"
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
def get_grupo_empleados(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = GrupoEmpleadosController(db).get_grupo_empleados(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Grupo de Empleados":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Grupo de Empleados no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Grupo de Empleados no encontrado"})      


# ruta para listar los datos historicos de la sociedades por ID
@grupos_empleados_router.get ('/grupo_empleados/{id}/list_historico', 
tags=["Grupos Empleados"],
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
def list_history_grupo_empleados(page : int = 1, records : int = 20, id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de grupos  en un resultset
    result = GrupoEmpleadosController(db).list_history_grupo_empleados(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar una sociedad por nombre o rut
@grupos_empleados_router.get ('/search_grupo', 
tags=["Grupos Empleados"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupo de Empleados encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Empleados encontrado",
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
def search_grupo_empleados(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = GrupoEmpleadosController(db).search_grupo_empleados(finding)
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


# ruta para actualizar un grupo de empleado por Id
@grupos_empleados_router.put ('/grupo_empleados/{id}/update', 
tags=["Grupos Empleados"],
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
def update_grupo_empleados(sociedad:GruposEmpleadoSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = GrupoEmpleadosController(db).update_grupo_empleados(sociedad, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=200,content={"message":"Sociedad actualizada","Sociedad":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
