'''
Esquema de datos que define a la tabla de datos de colación del usuario
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a los datos de colacion del usuario en el sistema
class ColacionUser(BaseModel):
    sociedad_id: int = Field (ge=1,lt=1000)
    user_id: int = Field (ge=1,lt=20000)
    movilizacion : float
    colacion  : float
    familiar  : float    
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'sociedad_id': 1,
                    'user_id': 1,
                    'movilizacion' : 0,
                    'colacion'  : 0,
                    'familiar'  : 0  
                }
            ]
        }
    }    
