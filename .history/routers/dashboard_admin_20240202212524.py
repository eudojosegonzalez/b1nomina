'''
Rutas de Dashboard Admin
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

from controller.dashboard_admin import DashboardAdminController as dashboardAdminController


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer



# esta variable define al router
dashboard_admin_router = APIRouter(prefix="/V1.0")


# ruta para consultar los datos inicales del dashboard 
@dashboard_admin_router.get ('/dashboard_admin_home', 
tags=["DashboardAdmin"],
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
def list_home_variables():
    db = Session()
    result=dashboardAdminController(db).count_users()

    if (result['result']=="1"):
        nRecordUsers=result['nRecordUsers']
    else:
        nRecordUsers="N/A"
    homeValues={
        "CostosNomina":0.00,
        "Bonificaciones":0.00,
        "Asignaciones":0.00,
        "Deducciones":0.00,
        "TotalUsers":nRecordUsers,
        "SueldoMinimo":450000.00,
        "SeguroAFC1":2.00,
        "SeguroAFC2":0.6,
        "TopeImposicion":81.60 
    }
    return JSONResponse (status_code=201,content={"initialValues":homeValues})  


# funcion que permite extraer el resumen de los empelados
@dashboard_admin_router.get ('/user/resumen_empleados',
tags=["DashboardAdmin"],
dependencies=[Depends(JWTBearer())],
responses=
    { 
        200: {
                "description": "Resumen de los Empleados",
                "content": { 
                    "application/json":
                        { 
                            "example":
                                {                           
                                    "message":"Resumen de los Empleados",
                                    "data": "{'empleados':'100','contratacion':'5', 'inactivos':'1'}",
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
            "description": "Usuario no encontrado",
            "content": { 
                "application/json":{ 
                    "example":
                        {
                            "message":"Usuario no encontrado"
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
def get_resumen_empleados():
    db = Session()
    # almacenamos el listado de usarios en un resultset
    result = dashboardAdminController(db).get_employee_summary()
    # debemnos convertir los objetos tipo BD a Json
    if (result):
        if (result["result"]=="1"):
            data=result['data']
            return JSONResponse(status_code=200,content=jsonable_encoder(data))    
        else:
            return JSONResponse(status_code=404,content={"message":"Este usuario no tiene modulos asignados"})     
    
    
    return JSONResponse(status_code=404,content={"message":"Este usuario no tiene modulos asignados"})   
  

