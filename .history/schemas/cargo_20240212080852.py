'''
Esquema de datos que define a la tabla Cargos
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Cargos(BaseModel):
    nombre : str = Field(min_length=2, max_length=250)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre":"Cargo Demo"
                }
            ]
        }
    }    
