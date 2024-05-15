'''
Esquema de datos que define a la tabla Datos Laborales A
Created 2024-02
'''
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

#Esquema de datos que represnta el fromulario de datos Laborales A
class DatosLaboralesSalario(BaseModel):
    salario_base :  int = Field(ge=1)   
    unidad_sueldo : int = Field (ge=1, le=2)
    monto_sueldo : float =Field (ge=500000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "salario_base":30,
                    "unidad_sueldo":1,
                    "monto_sueldo":500000
                }
            ]
        }
    }
   
