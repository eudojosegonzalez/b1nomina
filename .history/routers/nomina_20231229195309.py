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


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer


# esta variable define al router
nomina_router = APIRouter(prefix="/V1.0")

# -------- Rutas AFP ------------
# ruta para crear las Instituciones AFP
@nomina_router.post ('/create_nomina', tags=["Nomina"], dependencies=[Depends(JWTBearer())])
def create_payroll():
    return JSONResponse (status_code=201,content={"message":"Se creo una nómina en el sistema"})  
 
     
