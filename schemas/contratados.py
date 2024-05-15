'''
Esquema de datos que define a la tabla Contratadis
Created 2024-04
'''
from pydantic import BaseModel, Field
from typing import  Optional, List


#clase que representa los datos de contacto del  usuario en el sistema
class Contratados(BaseModel):
    sociedad_id: int = Field (ge=1,lt=1000)    
    user_id: int = Field (ge=1,lt=20000)

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
