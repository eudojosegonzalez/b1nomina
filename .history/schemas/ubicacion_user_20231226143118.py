# Schema de datos de Ubicación del Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Ubicación del Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa la localización geográfica del usuario en el sistema
class ContactUser(BaseModel):
    id : int = Field (ge=1, lt= 20000)
    user_id: int = Field (ge=1, lt=20000)
    region_id: int = Field (ge=1, lt=2000)
    comuna_id: int = Field (ge=1, lt=2000)
    direccion: str = Field (min_length= 0, max_length= 250)
  
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "region_id": 1,                    
                    "comuna_id": 1,
                    "direccion" : "alguna dirección"
                }
            ]
        }
    }    
