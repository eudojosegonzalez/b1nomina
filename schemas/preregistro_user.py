# Schema de datos de Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa a un usuario en el sistema
class PreUser(BaseModel):
    documento: str = Field (min_length=3, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellidos :str   = Field (min_length=2, max_length=100)
    correo :str   = Field (min_length=3, max_length=250)


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documento": "12345678912",
                    "nombres": "Pedro ",
                    "apellidos" : "Perez",
                    "correo":"example@correo.com"
                }
            ]
        }
    }    
