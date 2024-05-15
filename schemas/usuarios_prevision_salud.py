'''
Esquema de datos que define a la tabla Usuarios Prevision Salud
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class UsuariosPrevicionSalud(BaseModel):
    prevision_salud_id : int = Field(ge=1, le=100)
    user_id : int = Field(ge=1, le=2000)
    pactado : float    
    tipo_contrato : int = Field (ge=1, le=2)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prevision_salud_id" : 1,
                    "user_id" : 1,
                    "pactado" : 0.00 ,                  
                    "tipo_contrato" : 1,

                }
            ]
        }
    }    
 