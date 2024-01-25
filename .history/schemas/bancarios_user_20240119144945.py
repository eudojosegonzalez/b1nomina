'''
Esquema de datos que define a la tabla Bancarios del usuario
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un usuario en el sistema
class BancarioUser(BaseModel):
    id: int = Field (ge=1,lt=20000)
    user_id: int = Field (ge=1,lt=20000)
    banco_id : int = Field(gr=1, lt=1000)
    numero_cuenta : str = Field (min_length=3, max_length=100)
    en_uso : int
    terceros : int
    rut_tercero : str = Field (max_length=100)
    nombre_tercero: str = Field (max_length=100)
    email_tercero  : str = Field (max_length=250)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":1,
                    "user_id": 1,
                    "banco_id": 1,
                    "numero_cuenta": "18800023158",
                    "en_uso" : 1,
                    "terceros":1,
                    "rut_tercero":"26337084-8",
                    "nombre_tercero":"Sergio Rivas",
                    "email_tercero": "example@micorreo.com"
                }
            ]
        }
    }    
