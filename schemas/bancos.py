'''
Esquema de datos que define a la tabla Bancos
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un Banco en el sistema
class Bancos(BaseModel):
    codigo : str = Field(min_length=3, max_length=50)
    nombre : str = Field(min_length=3, max_length=150)
    nomina : bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo": "001",
                    "nombre":"BANCO CHILE Y EDWARDS",
                    "nomina": 1
                }
            ]
        }
    }    
