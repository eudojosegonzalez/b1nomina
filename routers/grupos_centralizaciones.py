'''
Rutas de Grupos Centralizaciones
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

#importamos el grupo de centralizacion
from schemas.grupos_centralizaciones import GrupoCentralizaciones  as GrupoCentralizacionesSchema

# importamos el controlador 
from controller.grupos_centralizaciones import GrupoCentralizacionesController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

#cargamos las variables de entorno
dotenv.load_dotenv()


# esta variable define al router
grupos_centralizaciones_router = APIRouter(prefix="/V1.0")

# -------- Rutas Grupos de Centralizaciones ------------
# ruta para crear el grupo de centralizacion
@grupos_centralizaciones_router.post ('/create_grupo_centralizacion', 
tags=["Grupos Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
            "description": "Se creo un Grupo de Centralización en el sistema",
            "content": { 
                "application/json":{
                    "example":
                        {
                            "message":"Se creo un Grupo de Centralización en el sistema",
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
def create_grupo_centralizacion(grupoCentralizacion:GrupoCentralizacionesSchema, userCreatorId : int = Query (ge=1, le=os.getenv("MAX_ID_USERS")))->dict:
    db = Session()
    result=GrupoCentralizacionesController(db).create_grupo_centralizaciones(grupoCentralizacion,userCreatorId)
    # evaluamos el resultado
    estado=result['result']

    if (estado=="1") :
        # se inserto el registro sin problemas
        newSociedad=result['data']
        return JSONResponse (status_code=201,content={"message":"Se creo un Grupo de Centralización en el sistema","Sociedad":jsonable_encoder(newSociedad)})     
    elif  (estado=="-1"):
        # el username ya existe no puede volver a insertarlo
        return JSONResponse (status_code=521,content={"message":"existe un Grupo de Centralización con este nombre, no puede volver a crearla","Sociedad":jsonable_encoder(result['data'])})     
    else:
        return JSONResponse (status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado","estado":result})    
             


# ruta para consultar un Grupo de Centralización por Id
@grupos_centralizaciones_router.get ('/grupo_centralizacion/{id}', 
tags=["Grupos Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupo de Centralización encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Centralización",
                                    "data": "{'id': '1', 'sociedad_id': '1', 'es_honorario': '1', 'nombre': 'DEMO', 'monto_max_prestamo': '0', 'cuotas_max_prestamo ': '0', 'porcentaje_tope_cuota_prestamo': '0', 'monto_max_anticipo': '0', 'porcentaje_maximo_anticipo': '0', 'calcular_porcentaje_segun': '', 'factura_mas_pago ': '0', 'cuenta_factura_proveedor': '', 'cuenta_pago_factura': '', 'cuenta_remunera_deb': '', 'cuenta_AFP_deb': '', 'cuenta_salud_deb': '', 'cuenta_gratificacion_deb ': '', 'cuenta_horas_ext_deb': '', 'cuenta_seg_AFC_deb': '', 'cuenta_mov_deb': '', 'cuenta_col_deb': '', 'cuenta_otra_asig_deb': '', 'cuenta_SIS_deb': '', 'cuenta_mut_deb': '', 'cuenta_impuesto_unico_deb': '', 'cuenta_asignacion_fami_deb': '', 'cuenta_Afc_empresa_cred': '', 'cuenta_asignacion_familiar_cred': '', 'cuenta_impuesto_unico_cred': '', 'cuenta_sueldo_pagar_cred': '', 'created': '2024-04-05 11:26:04', 'updated': '2024-04-05 11:26:04', 'creator_user': '1', 'updater_user': '1'}"
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
def get_grupo_centralizacion(id: int):
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = GrupoCentralizacionesController(db).get_grupo_centralizaciones(id)
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content={"Grupo de Centralización":jsonable_encoder(data)})    
        else:
            return JSONResponse(status_code=404,content={"message":"Grupo de Centralización no encontrada"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Grupo de Centralización no encontrado"})      


# ruta para listar los datos historicos de la sociedades por ID
@grupos_centralizaciones_router.get ('/grupo_centralizacion/{id}/list_historico', 
tags=["Grupos Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupo de Centralización encontrada",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Centralización",
                                    "data": "{'id': '1', 'sociedad_id': '1', 'es_honorario': '1', 'nombre': 'DEMO', 'monto_max_prestamo': '0', 'cuotas_max_prestamo ': '0', 'porcentaje_tope_cuota_prestamo': '0', 'monto_max_anticipo': '0', 'porcentaje_maximo_anticipo': '0', 'calcular_porcentaje_segun': '', 'factura_mas_pago ': '0', 'cuenta_factura_proveedor': '', 'cuenta_pago_factura': '', 'cuenta_remunera_deb': '', 'cuenta_AFP_deb': '', 'cuenta_salud_deb': '', 'cuenta_gratificacion_deb ': '', 'cuenta_horas_ext_deb': '', 'cuenta_seg_AFC_deb': '', 'cuenta_mov_deb': '', 'cuenta_col_deb': '', 'cuenta_otra_asig_deb': '', 'cuenta_SIS_deb': '', 'cuenta_mut_deb': '', 'cuenta_impuesto_unico_deb': '', 'cuenta_asignacion_fami_deb': '', 'cuenta_Afc_empresa_cred': '', 'cuenta_asignacion_familiar_cred': '', 'cuenta_impuesto_unico_cred': '', 'cuenta_sueldo_pagar_cred': '', 'created': '2024-04-05 11:26:04', 'updated': '2024-04-05 11:26:04', 'creator_user': '1', 'updater_user': '1','fecha_registro':'2024-01-01 10:00','observaciones',''}"
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
def list_history_grupo_centralizacion(id : int =Path(ge=1, lt=1000))->dict:
    db = Session()
    # almacenamos el listado de grupos  en un resultset
    result = GrupoCentralizacionesController(db).list_history_grupo_centralizaciones(id)

    # debemos convertir los objetos tipo BD a Json
    if (result):
        return JSONResponse(status_code=200,content=jsonable_encoder(result))    
    else:
        return JSONResponse(status_code=404,content={"message":"No hay registros que mostrar"}) 


# ruta para buscar un Grupo de Centralización por nombre o rut
@grupos_centralizaciones_router.get ('/search_grupo_centralizacion', 
tags=["Grupos Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Grupo de Centralización encontrado",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Centralización encontrado",
                                    "data": "{'id': '1', 'sociedad_id': '1', 'es_honorario': '1', 'nombre': 'DEMO', 'monto_max_prestamo': '0', 'cuotas_max_prestamo ': '0', 'porcentaje_tope_cuota_prestamo': '0', 'monto_max_anticipo': '0', 'porcentaje_maximo_anticipo': '0', 'calcular_porcentaje_segun': '', 'factura_mas_pago ': '0', 'cuenta_factura_proveedor': '', 'cuenta_pago_factura': '', 'cuenta_remunera_deb': '', 'cuenta_AFP_deb': '', 'cuenta_salud_deb': '', 'cuenta_gratificacion_deb ': '', 'cuenta_horas_ext_deb': '', 'cuenta_seg_AFC_deb': '', 'cuenta_mov_deb': '', 'cuenta_col_deb': '', 'cuenta_otra_asig_deb': '', 'cuenta_SIS_deb': '', 'cuenta_mut_deb': '', 'cuenta_impuesto_unico_deb': '', 'cuenta_asignacion_fami_deb': '', 'cuenta_Afc_empresa_cred': '', 'cuenta_asignacion_familiar_cred': '', 'cuenta_impuesto_unico_cred': '', 'cuenta_sueldo_pagar_cred': '', 'created': '2024-04-05 11:26:04', 'updated': '2024-04-05 11:26:04', 'creator_user': '1', 'updater_user': '1'}",
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
def search_grupo_centralizacion(finding : str = Query (min_length=os.getenv("MIN_STR_SEARCH_USER"), max_length=os.getenv("MAX_STR_SEARCH_USER")))->dict:
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = GrupoCentralizacionesController(db).search_grupo_centralizacion(finding)
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
@grupos_centralizaciones_router.put ('/grupo_centralizacion/{id}/update', 
tags=["Grupos Centralizaciones"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        201: {
                "description": "Grupo de Centralización actualizaco",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {
                                    "message":"Grupo de Centralización actualizado",
                                    "data": "{'id': '1', 'sociedad_id': '1', 'es_honorario': '1', 'nombre': 'DEMO', 'monto_max_prestamo': '0', 'cuotas_max_prestamo ': '0', 'porcentaje_tope_cuota_prestamo': '0', 'monto_max_anticipo': '0', 'porcentaje_maximo_anticipo': '0', 'calcular_porcentaje_segun': '', 'factura_mas_pago ': '0', 'cuenta_factura_proveedor': '', 'cuenta_pago_factura': '', 'cuenta_remunera_deb': '', 'cuenta_AFP_deb': '', 'cuenta_salud_deb': '', 'cuenta_gratificacion_deb ': '', 'cuenta_horas_ext_deb': '', 'cuenta_seg_AFC_deb': '', 'cuenta_mov_deb': '', 'cuenta_col_deb': '', 'cuenta_otra_asig_deb': '', 'cuenta_SIS_deb': '', 'cuenta_mut_deb': '', 'cuenta_impuesto_unico_deb': '', 'cuenta_asignacion_fami_deb': '', 'cuenta_Afc_empresa_cred': '', 'cuenta_asignacion_familiar_cred': '', 'cuenta_impuesto_unico_cred': '', 'cuenta_sueldo_pagar_cred': '', 'created': '2024-04-05 11:26:04', 'updated': '2024-04-05 11:26:04', 'creator_user': '1', 'updater_user': '1'}",
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
def update_grupo_centralizacion(grupoCentralizacion:GrupoCentralizacionesSchema, user_updater: int = Query(ge=1, le=os.getenv('MAX_ID_USERS')), id : int = Path(ge=1,le=1000))->dict:
    db = Session()
    # buscamos el registro
    result = GrupoCentralizacionesController(db).update_grupo_centralizaciones(grupoCentralizacion, user_updater, id) 
    if (result['result']=="1"):
        data=result['data']
        return JSONResponse(status_code=201,content={"message":"Grupo de Centralización actualizado","Grupo de Centralización":jsonable_encoder(data)})    
    elif (result['result']=="-1"):
        return JSONResponse(status_code=404,content={"message":"Usuario no encontrado"}) 
    else:
        return JSONResponse(status_code=520,content={"message":"Ocurrió un error que no pudo ser controlado"})        
