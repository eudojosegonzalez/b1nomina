'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Periodos(BaseModel):
    anio : int = Field(ge=1990, le=1000),
    mes : int = Field(ge=1, le=12),
    nombre : str = Field(min_length=3, max_length=250),
    direccion : str = Field(min_length=3, max_length=500),
    region_id : int = Field(ge=1, le=1000),
    comuna_id : int = Field(ge=1, le=1000),
    ciudad : str = Field(min_length=3, max_length=250),

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"Sede Demo",
                    "direccion": "Direccion Sede Demo",
                    "region_id": 1,
                    "comuna_id": 1101,
                    "ciudad":"Demo ciudad"
                }
            ]
        }
    }    


'''
	`anio` integer NOT NULL ,
	`mes` integer NOT NULL ,  
	`nombre` varchar(200) NOT NULL ,
	`observaciones` text NULL ,  
	`activo` boolean NULL,    
	`utm` numeric(18,4) default NULL,  
	`uf` numeric(18,4) default NULL,    
	`factor_actualizacion` numeric(18,4) default NULL,  
'''