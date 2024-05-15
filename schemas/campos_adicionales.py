'''
Esquema de datos que define a la tabla Campos Adicionales de la Sociedad
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class CamposAdicionales(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    camuser1 : str = Field (min_length=0, max_length=200)
    activo1 : int = Field(ge=0,le=1)
    camuser2 : str = Field (min_length=0, max_length=200)
    activo2 : int = Field(ge=0,le=1)
    camuser3 : str = Field (min_length=0, max_length=200)
    activo3 : int = Field(ge=0,le=1)
    camuser4 : str = Field (min_length=0, max_length=200)
    activo4 : int = Field(ge=0,le=1)
    camuser5 : str = Field (min_length=0, max_length=200)
    activo5 : int = Field(ge=0,le=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "camuser1" : ""  ,
                    "activo1":0,
                    "camuser2" : ""  ,
                    "activo2":0,
                    "camuser3": ""  ,
                    "activo3":0,                    
                    "camuser4" : ""  ,
                    "activo4":0,
                    "camuser5" : "",  
                    "activo5":0,
                }
            ]
        }
    }    
