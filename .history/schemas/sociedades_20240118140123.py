'''
Esquema de datos que define a la tabla Sociedades
Created 2024-01
'''
from pydantic import BaseModel, Field
'''
	id	bigint(20) AI PK
	rut	varchar(100)
	nombre	varchar(200)
	direccion	text
	region_id	bigint(20)
	comuna_id	bigint(20)
	ciudad	varchar(250)
	icono	varchar(250)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)
'''


#clase que representa a un usuario en el sistema
class Sociedades(BaseModel):
    rut : str = Field(min_length=3, max_length=100),
    nombre : str = Field(min_length=3, max_length=250),
    direccion : str = Field(min_length=3, max_length=500),
    region_id : int = Field(ge=1, le=1000),
    comuna_id : int = Field(ge=1, le=1000),
    ciudad : str = Field(min_length=3, max_length=250),
    icono : str = Field(min_length=3, max_length=250),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rut": "RutDemo",
                    "nombre":"Demo",
                    "direccion": "Direccion Demo",
                    "region_id": 1,
                    "comuna_id": 1,
                    "ciudad":"Demo ciudad",
                    'icono':''
                }
            ]
        }
    }    
