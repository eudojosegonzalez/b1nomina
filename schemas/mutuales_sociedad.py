'''
Esquema de datos que define a la tabla Mutuales de la Sociedad
Created 2024-03
'''
from pydantic import BaseModel, Field


#clase que representa a  alos datos bancarios del usuario en el sistema
class MutalesSociedad(BaseModel):
    sociedad_id: int = Field (ge=1,lt=20000)
    mutual_id : int = Field(gr=1, lt=1000)
    porcentaje : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": '1',
                    "mutual_id" : '1',
                    "porcentaje" : 0
                }
            ]
        }
    }    
