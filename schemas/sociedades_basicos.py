'''
Esquema de datos que define a la tabla Sociedades
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class SociedadesBasico(BaseModel):
    rut : str = Field(min_length=3, max_length=100)
    nombre : str = Field(min_length=3, max_length=250)
    direccion : str = Field(min_length=3, max_length=500)
    region_id : int = Field(ge=1, le=1000)
    comuna_id : int = Field(ge=1101)
    ciudad : str = Field(min_length=3, max_length=250)
    email : str = Field(min_length=0, max_length=250)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "rut": "RutDemo",
                    "nombre":"Demo",
                    "direccion": "Direccion Demo",
                    "region_id": 1,
                    "comuna_id": 1101,
                    "ciudad":"Demo ciudad",
                    'email':''
                }
            ]
        }
    }    
