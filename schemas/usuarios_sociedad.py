'''
Esquema de datos que define a la tabla Usuarios Grupos
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class UsuariosSociedad(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    user_id : int = Field(ge=1, le=2000) 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "user_id": 1,
                }
            ]
        }
    }    
