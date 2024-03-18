'''
Esquema de datos que define a la tabla NivelEstudio
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class NivelEstudio(BaseModel):

    descripcion : str = Field(min_length=3, max_length=150)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "descripcion":"Universitaria",
                }
            ]
        }
    }    
