'''
Esquema de datos que define a la tabla Departamentos
Created 2024-02
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Departamentos(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    sede_id : int = Field(ge=1, le=1000)   
    nombre : str = Field(min_length=3, max_length=250)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "sede_id": 1,
                    "nombre":"Departamento Demo"
                }
            ]
        }
    }    
