'''
Esquema de datos que define a la tabla Usuarios AFP
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class UsuariosAFP(BaseModel):
    user_id : int = Field(ge=1, le=2000)
    afp_id : int = Field (ge=1, le=100)
    jubilado_afp : int = Field(ge=0,le=1)
    ahorro_afp2 : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "afp_id" : 1,
                    "jubilado_afp" : 0,
                    "ahorro_afp2" : 0.00
                }
            ]
        }
    }    
