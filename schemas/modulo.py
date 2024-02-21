'''
Esquema de datos que define a la tabla Modulo del sistema
Created 2024-01
'''
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa la localización geográfica del usuario en el sistema
class Modulo(BaseModel):
    id : int = Field (ge=1, lt= 20000)
    nombre: str = Field (min_length= 3, max_length= 250)
    url : str  = Field (min_length= 0, max_length= 250)
    icono = Field (min_length= 3, max_length= 250)
    estado = bool      
  
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre" : "Nombre Módiulo",
                    "url" : "/",
                    "icono" : "",
                    "estado" : True,
                }
            ]
        }
    }    
