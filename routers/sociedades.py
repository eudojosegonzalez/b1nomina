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

#importamos el Sede
from schemas.sociedades import Sociedades as SocidadeSchema
from schemas.sociedades_basicos import SociedadesBasico as  SociedadesBasicoSchema
from schemas.sociedades_representante import SociedadesRepresentante as SociedadesRepresentanteSchema
from schemas.sdg import SDG as SDGSchema


# importamos el controlador 
from controller.sociedades import sociedadesController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
sociedades_router = APIRouter(prefix="/V1.0")

# -------- Rutas Sedes ------------
# ruta para crear las Sociedades
@sociedades_router.post ('/create_sociedad', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Sociedad en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Sociedad en el sistema",
                            "newSociedad":"1"
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
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Sociedad encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sociedad encontrada",
                                    "data": "{ 'id': '1','rut': '123456789','direccion': 'SANTIAGO','comuna_id': '1101','icono': '','updated': '2024-01-18T16:02:45','updater_user': '1','region_id': '1','nombre': 'DEMO','ciudad': 'DEMO CIUDAD','created': '1990-01-01T00:00:00', 'creator_user': '1'}"
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
def get_sociedad(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_sociedad(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Sociedad":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})      


# ruta para consultar dstos basicos de una sociedad por Id
@sociedades_router.get ('/sociedad/{id}/datos_basicos', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Sociedad encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sociedad encontrada",
                                    "data": "{ 'id': '1','rut': '123456789','direccion': 'SANTIAGO','comuna_id': '1101','icono': '','updated': '2024-01-18T16:02:45','updater_user': '1','region_id': '1','nombre': 'DEMO','ciudad': 'DEMO CIUDAD','created': '1990-01-01T00:00:00', 'creator_user': '1'}"
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
def get_sociedad_basicos(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_sociedad_basicos(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Sociedad":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})      


# ruta para consultar dstos basicos de una sociedad por Id
@sociedades_router.get ('/sociedad/{id}/datos_representante', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sociedad encontrada",
                                    "data": "{ 'id': '1','rut': '123456789','direccion': 'SANTIAGO','comuna_id': '1101','icono': '','updated': '2024-01-18T16:02:45','updater_user': '1','region_id': '1','nombre': 'DEMO','ciudad': 'DEMO CIUDAD','created': '1990-01-01T00:00:00', 'creator_user': '1'}"
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
def get_sociedad_representante(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_sociedad_representante(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Sociedad":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Sociedad no encontrada"})      



# ruta para listar los datos de las sedes por ID
@sociedades_router.get ('/sociedad/{id}/list_sede', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Sedes encontradas",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Sedes encontradas",
                                    "data": "{'id': '1','direccion': 'DIRECCION SEDE DEMO','comuna_id': '1101','created': '2024-02-01T13:13:35','creator_user': '1','region_id': '1','sociedad_id': '1','nombre': 'SEDE UNO','ciudad': 'DEMO CIUDAD','updated': '2024-02-01T13:14:54','updater_user': '1'}",
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
def list_sociedad_sedes(page : int = 1, records : int = 20, id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_sociedad_sedes(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar los datos de los departamentos de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_departamentos', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Departamentos Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Departamentos Encontrados",
                                    "data": "{'sociedad_id': '1','sede_id': '1','created': '2024-02-01T10:00:00','creator_user': '1','nombre': 'Administración','id': '1','updated': '2024-02-01T10:00:00','updater_user': '1'}",
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
def list_sociedad_departamentos(page : int = 1, records : int = 20, id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de los departamentos en un resultset
    result = sociedadesController(db).list_sociedad_departamentos(page,records,id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    


# ruta para listar los datos de las cuentas contables de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_cuentas_contables', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Cuentas Contables Encontradas",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Cuentas Contables Encontradas",
                                    "data": "{'id': '1','sociedad_id': '1','acct_code': '11010001','acct_name': 'Caja','finance': 'Y','created': '2024-02-20T10:00:00','updated': '2024-02-20T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_sociedad_cuentas_contables(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de los departamentos en un resultset
    result = sociedadesController(db).list_sociedad_cuentas_contables(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar los datos de los grupos de empleados de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_grupos_empleados', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupos Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupos Encontrados",
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'Administrativo','updated': '2024-02-05T10:00:00','updater_user': '1','es_honorario': '0','created': '2024-02-05T10:00:00','creator_user': '1'}",
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
def list_sociedad_grupos_empleados( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de grupos en un resul set
    result = sociedadesController(db).list_sociedad_grupos_empleados(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    
    


# ruta para listar los datos de los empleados de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_empleados', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Empleados Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Empleados Encontradoss",
                                    "data": "{'sociedad_id': '1','sede_id': '1','created': '2024-02-01T10:00:00','creator_user': '1','nombre': 'Administración','id': '1','updated': '2024-02-01T10:00:00','updater_user': '1'}",
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
def list_sociedad_empleados( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_sociedad_empleados(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    
    
# ruta para listar los datos de los empleados de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_no_empleados', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Encontradoss",
                                    "data": "{'id': 2,'nombre': 'PEDRO','apellido_paterno': 'PEREZ', 'apellido_materno': 'MARTINEZ', 'activo': false, 'cargo': 'No Asignado', 'sueldo': '0', 'rut': '12345678912', 'cv_estatus': '1', 'contrato_estatus': '1', 'avance': 34}",
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
async def list_sociedad_no_empleados( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_sociedad_no_empleados(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar los datos de los empleados de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_empleados_inactivos', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Encontradoss",
                                    "data": "{'sociedad_id': '1','sede_id': '1','created': '2024-02-01T10:00:00','creator_user': '1','nombre': 'Administración','id': '1','updated': '2024-02-01T10:00:00','updater_user': '1'}",
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
def list_sociedad_no_empleados( id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_sociedad_empleados_inactivos(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        
        

# Funcion para efectuar busquedas en la vista viewGeneralUser
# se efectuan busquedas del tipo LIKE en la vista
@sociedades_router.post ('/sociedad/{id}/searchsdg',
tags=['Sociedades'],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Usuario encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Usuario encontrado",
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
async def   search_users_sdg(sdg : SDGSchema, id : int =Path(ge=1, lt=1000) )->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    sede_id=sdg.sede_id
    departamento_id=sdg.departamento_id
    grupo_id=sdg.grupo_id
    result = sociedadesController(db).search_users_sdg2(id,sede_id,departamento_id,grupo_id)

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
    
    

# ruta para listar loas categorias de configuracion de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_categorias_configuracion', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Categorias de Configuracion Encontradas",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Categorias de Configuracion Encontradas",
                                    "data": "{'id': '1','sociedad_id': '1','nombre': 'CONFIGURACIONES BASICAS','activo': 'true','created': '2024-02-13T10:00:00','updated': '2024-02-13T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_sociedad_categorias_configuracion(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de la consulta
    result = sociedadesController(db).list_sociedad_categorias_configuracion(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar loas categorias de configuracion de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_configuraciones', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Categorias de Configuracion Encontradas",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Categorias de Configuracion Encontradas",
                                    "data": "{'id': '1','nombre': 'Sueldo Minimo ($)','detalle': '','ocultar': '0','orden': '1','updated': '2024-02-19T10:00:00','updater_user': '1','valor': '445000','sociedad_id': '1',  'categoria_id': '1','cuenta': '','tipo_validacion': 'Numérico','created': '2024-02-19T10:00:00','creator_user': '1'}",
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
def list_sociedad_configuraciones(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de la consulta
    result = sociedadesController(db).list_sociedad_configuraciones(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    


# ruta para listar los tipos de prestamos de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/list_tipos_prestamos', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Tipo de Prestamo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Tipo de Prestamo Encontrado",
                                    "data": "{'id': '2','sociedad_id': '1','descripcion': 'CCAF','CCAF': '1','cuenta': '21050003','caja_compensacion_id': 'null','created': '2024-02-21T10:00:00','updated': '2024-02-21T10:00:00','creator_user': '1','updater_user': '1'}",
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
def list_tipos_prestamos_sociedad(id : int = Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_tipos_prestamos_sociedad(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    


# ruta para listar los parametros de creacion de usuarios de una sociedad por ID
@sociedades_router.get ('/sociedad/{id}/parametros_crear_usuario', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Parametros",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"parametros",
                                    "data": "{[{'departamentos': [{'id': '1','nombres': 'Administración'},{'id': '2','nombres': 'Contabilidad'},{'id': '3','nombres': 'Ventas'}]},{'grupos': [{'id': '1','nombres': 'Administrativo'},{'id': '2','nombres': 'Ejecutivo'},{'id': '3','nombres': 'Operaciones'}]}]}",
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
def list_parametros_crear_usuario(id: int = Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_parametros_crear_usuario(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar los parametros de creacion de sociedades en el sistema
@sociedades_router.get ('/parametros_regionales', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Parametros",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"parametros",
                                    "data": "{'regiones': [{'id': 1,'nombre': 'Tarapacá'},{'id': 2,'nombre': 'Antofagasta'}],'localidad': [{'id': 1101,'nombre': 'Iquique','idregion': 1},{'id': 1107,'nombre': 'Alto Hospicio','idregion': 1}]}",
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
def list_parametros_crear_sociedad()->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_parametros_crear_sociedad()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})     
    
    

# ruta para listar los datos historicos de la sociedades por ID
@sociedades_router.get ('/sociedad/{id}/resumen_empleados', 
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
def get_resumen_empleados(id : int = Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_employee_summary(id)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar los datos historicos de la sociedades por ID
@sociedades_router.get ('/sociedad/{id}/list_historico', 
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
                "description": "Sedes encontrado",
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



# ruta para descargar el archivo de importacion de usuarios
@sociedades_router.get ('/sociedad/{id}/dowload_file_bulk_user', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Archivo Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Archivo Encontrado",
                                    "data": "massive_users/FormatoCargaEMP.xlsx",
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
def dowload_file_bulk_user(id : int = Path(ge=1,le=2000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).dowload_file_bulk_user(id)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            return JSONResponse(status_code=200,content={"data":"massive_users/FormatoCargaEMP.xlsx"})    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"La búsqueda no arrojó resultados"})    
        else:
            return JSONResponse(status_code=520,content={"message":"System Error","error":result})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})


# ruta para consultas los campos adicionales por sociedad
#ruta para consultar los grupos de centralizacion de una sociedad
@sociedades_router.get ('/sociedad/{id}/get_campos_adicionales', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Campos Adicionales Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Campos Adicionales Encontrado",
                                    "data": "[{'campo1': {'nombre': 'Campaña Uno','activo': 1}},{'campo2': {'nombre': '','activo': 0}},{'campo2': {'nombre': '','activo': 0}},{'campo4': {'nombre': '','activo': 0}},{'campo5': {'nombre': '','activo': 0}}]",
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
def get_campos_adicionales(id : int = Path(ge=1, le=2000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).list_campos_adicionales(id)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"message":"Campos Adicionales Encontrados","data":jsonable_encoder(data)})    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"No se han definido Campos Adicionales"})    
        else:
            cadenaError=result['cadenaError']
            return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudeo ser controlado {cadenaError}"})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})
    

#ruta para consultar los grupos de centralizacion de una sociedad
@sociedades_router.get ('/sociedad/{id}/get_centralizaciones', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos de Centralizacion Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Centralizacion Entonctrado",
                                    "data": "{'monto_max_prestamo': 0,'cuenta_pago_factura': '','cuenta_col_deb': '','cuenta_impuesto_unico_cred': '','cuotas_max_prestamo': 0,'cuenta_remunera_deb': '','cuenta_otra_asig_deb': '','cuenta_sueldo_pagar_cred': '','porcentaje_tope_cuota_prestamo': 0,'cuenta_AFP_deb': '','cuenta_SIS_deb': '','created': '2024-04-05T11:26:04','monto_max_anticipo': 0,'cuenta_salud_deb': '','cuenta_mut_deb': '','updated': '2024-04-05T11:26:04','sociedad_id': 1,'porcentaje_maximo_anticipo': 0,'cuenta_gratificacion_deb': '','cuenta_impuesto_unico_deb': '','creator_user': 1,'es_honorario': 1,'calcular_porcentaje_segun': '','cuenta_horas_ext_deb': '','cuenta_asignacion_fami_deb': '','updater_user': 1,'factura_mas_pago': 0,'cuenta_seg_AFC_deb': '','cuenta_Afc_empresa_cred': '','nombre': 'DEMO','id': 1,'cuenta_factura_proveedor': '','cuenta_mov_deb': '','cuenta_asignacion_familiar_cred': ''}",
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
def get_centralizaciones(id : int = Path(ge=1, le=2000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_centralizaciones(id)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"message":"Datos de Centralizacion Encontrados","data":jsonable_encoder(data)})    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"No se han definido centralizaciones"})    
        else:
            cadenaError=result['cadenaError']
            return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudeo ser controlado {cadenaError}"})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})


# ruta para buscar una sociedad por nombre o rut
@sociedades_router.get ('/sociedad/{id}/get_centralizaciones2', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos de Centralizacion Encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos de Centralizacion Entonctrado",
                                    "data": "[{'id': 1,'nombre': 'DEMO'},{'id': 2,'nombre': 'DEMO DOS'}]",
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
def get_centralizaciones2(id : int = Path(ge=1, le=2000))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = sociedadesController(db).get_centralizaciones2(id)
    # debemos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"message":"Datos de Centralizacion Encontrados","data":jsonable_encoder(data)})    
        elif (result["result"]=="-1"):
            return JSONResponse(status_code=404,content={"message":"No se han definido centralizaciones"})    
        else:
            cadenaError=result['cadenaError']
            return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudeo ser controlado {cadenaError}"})          
    else:
        return JSONResponse(status_code=520,content={"message":"System Error","error":result})



# -----------------------------------------------------------------------------------------
# rutas put
#------------------------------------------------------------------------------------------
# ruta para actualizar una sociedad por Id
@sociedades_router.put ('/sociedad/{id}/update', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
                "description": "Sociedad Actualizada",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Sociedad Actualziada",
                                "data":"{'id':1,'nombre':'Sociedad Uno'}"
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
def update_sociedad(sociedad:SocidadeSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = sociedadesController(db).update_sociedad(sociedad, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Sociedad actualizada","Sociedad":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        


# ruta para actualizar una sociedad por Id
@sociedades_router.put ('/sociedad/{id}/update_basicos', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
                "description": "Sociedad Actualizada",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Sociedad Actualziada",
                                "data":"{'id':1,'nombre':'Sociedad Uno'}"
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
def update_sociedad_basicos(sociedad:SociedadesBasicoSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = sociedadesController(db).update_sociedad_basicos(sociedad, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Sociedad actualizada","Sociedad":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})        
    


# ruta para actualizar una sociedad por Id
@sociedades_router.put ('/sociedad/{id}/update_representante', 
tags=["Sociedades"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
                "description": "Sociedad Actualizada",
                "content": { 
                    "application/json":{ 
                        "example":
                            {
                                "message":"Sociedad Actualziada",
                                "data":"{'id':1,'nombre':'Sociedad Uno'}"
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
def update_sociedad_representante(sociedad:SociedadesRepresentanteSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = sociedadesController(db).update_sociedad_representante(sociedad, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Sociedad actualizada","Sociedad":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})        