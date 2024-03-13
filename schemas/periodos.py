'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Periodos(BaseModel):
    anio : int = Field(ge=1990)
    mes : int = Field(ge=1, le=12)
    nombre : str = Field(min_length=3, max_length=250)
    observaciones: str = Field(min_length=0, max_length=500)
    activo : bool
    utm : float
    uf :float
    factor_actualizacion : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "anio": 2023,
                    "mes": 1,
                    "nombre":"Enero 2023",
                    "observaciones":"",
                    "activo":True,
                    "utm":47729.00,
                    "uf":28679.45,
                    "factor_actualizacion":1013
                }
            ]
        }
    }    