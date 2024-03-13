'''
Esquema de datos que define a la tabla Datos Laborales
Created 2024-02
'''
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

#clase que representa a una sociedad en el sistema
class DatosLaborales(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    sede_id : int = Field(ge=1, le=1000)
    departamento_id : int = Field(ge=1, le=1000)  
    grupo_id : int = Field(ge=0, le=1000)      
    cargo_id : int = Field(ge=1, le=1000)    
    user_id : int = Field(ge=1, le=10000)    
    tipo_contrato : int = Field(ge=1, le=2)    
    termino_contrato : int = Field(ge=1, le=2) 
    fecha_inicio : date = None
    fecha_fin : date = None
    periodo_salario: int
    modalidad: int    
    dias_descanso: str = Field (min_length=1, max_length=50)
    salario_base : float 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,                    
                    "departamento_id": 1,                    
                    "grupo_id":0,
                    "cargo_id":1,
                    "user_id":1,
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                     "fecha_fin":'',
                    "periodo_salario":30,
                    "modalidad":0,
                    "dias_descanso":"1",
                    "salario_base": 4500.00
                }
            ]
        }
    }
   
