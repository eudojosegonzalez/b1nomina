'''
Esquema de datos que define a la tabla Datos Laborales Adicionales y Centralizacion
Created 2024-04
'''
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

#clase que representa a una sociedad en el sistema
class DatosLaboralesAdicionales(BaseModel):
    grupo_centralizacion_id : int = Field(ge=1, le=1000)
    camuser1 : str = Field (min_length=0, max_length=200)
    camuser2 : str = Field (min_length=0, max_length=200)
    camuser3 : str = Field (min_length=0, max_length=200)
    camuser4 : str = Field (min_length=0, max_length=200)
    camuser5 : str = Field (min_length=0, max_length=200)    

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "grupo_centralizacion_id": 1,                    
                    "camuser1" : ""  ,
                    "camuser2" : ""  ,
                    "camuser3" : ""  ,
                    "camuser4" : ""  ,
                    "camuser5" : ""  
                }
            ]
        }
    }
   
