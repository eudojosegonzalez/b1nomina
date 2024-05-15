'''
Rutas de Datos Laborales
2024-02
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

#importamos el esquema de la sede
from schemas.datos_laborales import DatosLaborales as DatosLaboralesSchema

# importamos el controlador 
from controller.datos_laborales import DatosLaboralesController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
datos_laborales_router = APIRouter(prefix="/V1.0")

# -------- Rutas Datos laborales ------------
# ruta para crear las datos laborales
@datos_laborales_router.post ('/create_datos_laborales', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Dato Laboral sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Datos Laboral en el sistema",
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
        521: {
            "description": "Este usuario ya tiene Datos Laborales no puede volver a crearlo",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
                                }
                        } 
                    
                }       
            },                                
    }                      
)
def create_datos_laborales(datosLaborales:DatosLaboralesSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=DatosLaboralesController(db).create_datos_laborales(datosLaborales,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1"):
        # se inserto el registro sin problemas
        newDatoLaboral=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Dato Laboral en el sistema","Dato Laboral":jsonable_encoder(newDatoLaboral)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        datoLaboral=result['data']
        return JSONResponse (status_code=521,content={"message":"Este usuario ya tiene Datos Laborales no puede volver a crearlo","Dato Laboral Existente":jsonable_encoder(datoLaboral)})     

    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             

# ruta para listar los datos laborales en el sistema
@datos_laborales_router.get ('/list_datos_laborales', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales()->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_datos_laborales()

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar los datos laborales en el sistema segun la sociedad que las agrupa
@datos_laborales_router.get ('/list_datos_laborales_sociedad', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales_sociedad(idSociedad: int)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_datos_laborales_sociedad(idSociedad)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para listar los datos laborales  en el sistema segun la sede que los agrupa
@datos_laborales_router.get ('/list_datos_laborales_sede', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales_sede(idSede: int)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_datos_laborales_sede(idSede)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    


# ruta para listar los datos laborales  en el sistema segun el departamento que los agrupa
@datos_laborales_router.get ('/list_datos_laborales_departamento', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales_departamento(idDepartamento: int)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_datos_laborales_departamento(idDepartamento)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
    

# ruta para listar los datos laborales  en el sistema segun el grupo
@datos_laborales_router.get ('/list_datos_laborales_grupo', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales_grupo(idGrupo: int)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_datos_laborales_grupo(idGrupo)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        


# ruta para listar los datos laborales  en el sistema segun el user
@datos_laborales_router.get ('/get_datos_laborales_user', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
def list_datos_laborales_user(iduser: int)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).get_datos_laborales_userid(iduser)

    # debemnos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 
        



# ruta para consultar un dato laboral por Id
@datos_laborales_router.get ('/datos_laborales/{id}', 
tags=["Datos Laborales"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
            "description": "Dato Laboral no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Dato Laboral no encontrado"
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
def get_datos_laborales(id: int):
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).get_datos_laborales(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Dato Laboral encontrado":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Dato Laboral no encontrado"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Dato Laboral no encontrado"})      



# ruta para listar los datos historicos del dato laboral por ID
@datos_laborales_router.get ('/datos_laborales/{id}/list_historico', 
tags=["Datos Laborales"],

responses=
    { 
        200: {
                "description": "Datos Laborales Encontrados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Datos Laborales Encontrados",
                                    "data": "{'id': '6', 'sociedad_id': '1','sede_id': '1','departamento_id': '1','grupo_id': '1','cargo_id': '1','user_id': '1','tipo_contrato': '1','termino_contrato': '1','fecha_inicio': '2024-01-01','fecha_fin': '1999-01-01','periodo_salario': '30',  'modalidad': '1','dias_descanso': '1','salario_base': '4500','created': '2024-02-29 19:55:05','updated': '2024-02-29 19:55:05', 'creator_user': '1', 'updater_user': '1'}",
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
            "description": "No hay registros que mostrar",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"No hay registros que mostrar"
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
def list_history_datos_laborales(id)->dict:
    db = Session()
    # almacenamos el listado de datos laborales en un resultset
    result = DatosLaboralesController(db).list_history_datos_laborales(id)

    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Datos Laborales":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})     
    
    
    return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"})        



# ruta para actualizar un datos laboral por Id
@datos_laborales_router.put ('/datos_laborales/{id}/update', 
tags=["Datos Laborales"],
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
        404: {
            "description": "Dalo Laboral no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Dalo Laboral no encontrado"
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
def update_datos_laborales(datosLaborales:DatosLaboralesSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = DatosLaboralesController(db).update_datos_laborales(datosLaborales, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Dato laboral actualizado","sede":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Dato Laboral no encontrado"}) 
    else:
        cadenaError=result['cadenaError']
        return JSONResponse(status_code=520,content={"message":f"Ocurrió un error que no pudo ser controlado {cadenaError}"})        


