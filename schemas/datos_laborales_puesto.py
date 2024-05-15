'''
Esquema de datos que define a la tabla Datos Laborales
Created 2024-02
'''
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

#clase que representa a una sociedad en el sistema
class DatosLaboralesPuesto(BaseModel):
    sede_id : int = Field(ge=1, le=1000)
    departamento_id : int = Field(ge=1, le=1000)  
    grupo_id : int = Field(ge=0, le=1000)      
    cargo_id : int = Field(ge=1, le=1000)    
    modalidad: int    

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":1,
                    "cargo_id":1,
                    "modalidad":0,
                }
            ]
        }
    }
   
