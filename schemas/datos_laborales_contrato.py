'''
Esquema de datos que define a la tabla Datos Laborales A
Created 2024-02
'''
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

#Esquema de datos que represnta el fromulario de datos Laborales A
class DatosLaboralesContrato(BaseModel):
    tipo_contrato : int = Field(ge=1, le=2)    
    termino_contrato : int = Field(ge=0, le=1) 
    fecha_inicio : date = None
    fecha_fin : date = None
    dias_descanso: str = Field (min_length=1, max_length=50)
    nivel_estudio_id : int
    hora_ingreso : time
    hora_egreso : time   
    jefatura : int= Field (ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tipo_contrato":1,
                    "termino_contrato":1,
                    "fecha_inicio":'2024-01-01',
                    "fecha_fin":'1990-01-01',
                    "dias_descanso":"1",
                    "nivel_estudio_id":1,
                    "hora_ingreso" : "08:00",
                    "hora_egreso" : "18:00",    
                    "jefatura":0                 
                }
            ]
        }
    }
   
