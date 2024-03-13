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
    observaciones: str = Field(min_length=3, max_length=500),
    activo : bool ,
    utm: float ,
    uf:float ,
    factor_actualizacion: float

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
