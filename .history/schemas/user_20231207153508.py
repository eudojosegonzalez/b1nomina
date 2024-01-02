from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date

#clase que representa a un usuario en el sistema
class User(BaseModel):
    id : int = Field (ge=1, lt= 2000)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    apellido_materno : str = Field (min_length=2, max_length=100)
    username : str  = Field (min_length=5, max_length=200)   
    password : str = Field (min_length=8, max_length=200)
    estado :  int = Field (gt=0,le=1)    

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "apellido_paterno" : "Perez",
                    "apellido_materno" :  "Martinez",
                    "username":"pperez",
                    "password":"12345678" 
                    "estado":"1"   
                }
            ]
        }
    }    

