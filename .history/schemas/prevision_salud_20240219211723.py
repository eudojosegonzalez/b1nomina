'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class PrevisionSalud(BaseModel):

    sociedad_id : int = Field (ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=250)
    prevision_salud_cuenta : str = Field(min_length=3, max_length=150)
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=10)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"Banmédica",
                    "prevision_salud_cuenta": "21050002",
                    "codigo_direccion_trabajo": "3",
                }
            ]
        }
    }    
