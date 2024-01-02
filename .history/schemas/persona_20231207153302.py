from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date

#clase que representa a un usuario en el sistema
class User(BaseModel):
    id : int = Field (ge=1, lt= 2000)
    rut: str = Field (min_length=8, max_length=100)
    rut_provisorio : Optional[str]  = Field (min_length=8, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    apellido_materno : str = Field (min_length=2, max_length=100)
    fecha_nacimiento : date
    sexo_id : int  = Field (ge=1, le= 2)
    estado_civil_id : int  = Field (ge=1, le= 5)
    nacionalidad_id : int   = Field (ge=1, le= 200)
    username : str  = Field (min_length=5, max_length=200)   
    password : str = Field (min_length=8, max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "rut": "12345678912",
                    "nombres": "Pedro ",
                    "apellido_paterno" : "Perez",
                    "apellido_materno" :  "Martinez",
                    "fecha_nacimiento": "1990-01-01",
                    "sexo_id":"1",
                    "estado_civil_id":"1",
                    "nacionalidad_id":"1",
                    "username":"pperez",
                    "password":"12345678"    
                }
            ]
        }
    }    


# esta clase es suada par validar unicamente al usuario
class Credenciales(BaseModel):
    username : str  = Field (min_length=8, max_length=200)   
    password : str = Field (min_length=8, max_length=200)