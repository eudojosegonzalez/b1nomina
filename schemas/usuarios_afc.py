'''
Esquema de datos que define a la tabla Usuarios AFC
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class UsuariosAFC(BaseModel):
    user_id : int = Field(ge=1, le=2000)
    estado : int = Field(ge=0, le=1)
    antiguedad : int = Field(ge=0, le=1)
    vejez : int = Field(ge=0, le=1)
    invalidez : int = Field(ge=0, le=1)
    exinp : int = Field(ge=0, le=1)
 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "estado" : 1,
                    "antiguedad" : 1,
                    "vejez" : 0,
                    "invalidez" : 0,
                    "exinp" : 0
                }
            ]
        }
    }    
