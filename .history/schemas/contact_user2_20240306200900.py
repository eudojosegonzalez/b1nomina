'''
Esquema de datos que define a la tabla Contacto del usuario
Created 2023-12
'''
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa los datos de contacto del  usuario en el sistema
class ContactUser(BaseModel):
    id : int = Field (ge=1, lt= 20000)
    user_id: int = Field (ge=1,lt=20000)
    email : Optional[str]  = Field (min_length=0, max_length=250)
    fijo : Optional[str]  = Field (min_length=0, max_length=20) 
    movil : Optional[str]  = Field (min_length=0, max_length=20)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "email": "example@micorreo.com",                    
                    "fijo": "226656168",
                    "movil" : "939024766"
                }
            ]
        }
    }    
