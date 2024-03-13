'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class PrevisionSalud(BaseModel):

    sociedad_id : int = Field (ge=1, le=1000)
    codigo_externo: str =Field (min_length=0, max_length=50)
    nombre : str = Field(min_length=3, max_length=250)
    prevision_salud_cuenta : str = Field(min_length=3, max_length=150)
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=10)  

    '''
	id	bigint(20) AI PK
	codigo_externo	varchar(50)
	nombre	varchar(100)
	prevision_salud_cuenta	varchar(150)
	codigo_direccion_trabajo	varchar(10)
	created	datetime
	updated	datetime
	creator_user	bigint(20)
	updater_user	bigint(20)    
    '''

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "codigo_externo":'01',
                    "nombre":"Banmédica",
                    "prevision_salud_cuenta": "21050002",
                    "codigo_direccion_trabajo": "3",
                }
            ]
        }
    }    
