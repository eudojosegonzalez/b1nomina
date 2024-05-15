'''
Esquema de datos que define a la tabla Contacto/Ubicacion del usuario
Created 2024-05
'''
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa los datos de contacto del  usuario en el sistema
class ContactUbicationUser(BaseModel):
    email : Optional[str]  = Field (min_length=0, max_length=250)
    fijo : Optional[str]  = Field (min_length=0, max_length=20) 
    movil : Optional[str]  = Field (min_length=0, max_length=20)
    region_id: int = Field (ge=1)
    comuna_id: int = Field (ge=1101)
    direccion : Optional[str]  = Field (min_length=0, max_length=250)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@micorreo.com",                    
                    "fijo": "226656168",
                    "movil" : "939024766",
                    "region_id" : 1,
                    "comuna_id" : 1101,
                    "direccion" : ""
                }
            ]
        }
    }    
