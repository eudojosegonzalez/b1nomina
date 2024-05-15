'''
Esquema de datos que define a la tabla Grupos de Empleados
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class GruposEmpleado(BaseModel):
    sociedad_id : int = Field (min=1, max=100)
    es_honorario : bool
    nombre : str = Field(min_length=3, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "es_honorario": True,
                    "nombre":"Demo"
                }
            ]
        }
    }    
