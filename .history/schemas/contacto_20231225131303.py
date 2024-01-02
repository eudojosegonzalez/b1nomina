# Schema de datos de Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa a un usuario en el sistema
class Contact(BaseModel):
    id : int = Field (ge=1, lt= 2000)
    user_id : int = Field (ge=1, lt= 2000)
    email : str 
    fijo : str 
    movil : str 
    user : int = Field (ge=1, lt= 2000) 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": "1",
                    "email": "cuanta@micorreo.co,",
                    "fijo":"023222222",
                    "movil":"034333333",
                    "user":"1"
                }
            ]
        }
    }    
