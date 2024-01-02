# Schema de datos de Contacto del Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Contacto del Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa a un usuario en el sistema
class ContactUser(BaseModel):
    id : int = Field (ge=1, lt= 2000)
    user_id: int = Field (ge=1,lt=2000)
    email = Optional[str]  = Field (min_length=0, max_length=250)
    fijo = Optional[str]  = Field (min_length=0, max_length=20) 
    movil = Optional[str]  = Field (min_length=0, max_length=20)
    user : int = Field (ge=1, lt= 2000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": "1",
                    "email": "",                    
                    "fijo": "",
                    "movil" : "",
                    "user":1
                }
            ]
        }
    }    
