'''
Esquema de datos que define a la tabla Mutuales
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa una institucion mutual en el sistema
class Mutuales(BaseModel):
    nombre : str = Field(min_length=3, max_length=50),
    codigo_externo : str = Field(min_length=3, max_length=50),
    cuenta_contable : str = Field(min_length=3, max_length=50),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Asociación Chilena de seguridad (ACHS)",
                    "codigo_externo":"01",
                    "cuenta_contable": "21050004"
                }
            ]
        }
    }    

