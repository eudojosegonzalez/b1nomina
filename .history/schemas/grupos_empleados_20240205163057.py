'''
Esquema de datos que define a la tabla Sociedades
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Sociedades(BaseModel):
    es_honorario = bool,
    nombre : str = Field(min_length=3, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "es_honorario": True,
                    "nombre":"Demo"
                }
            ]
        }
    }    
