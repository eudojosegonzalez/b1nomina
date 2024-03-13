'''
Esquema de datos que define a la tabla Unidades de Pacto
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un Unidades de Pacto
class UnidadesPacto(BaseModel):
    descripcion : str = Field(min_length=1, max_length=150)
    estado : bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "descripcion":"UF",
                    "estado": True
                }
            ]
        }
    }    
