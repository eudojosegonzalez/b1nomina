'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class CategoriasConfiguracion(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=250)
    activo :  bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "nombre":"Configuracion Básica",
                    "activo": True,
                }
            ]
        }
    }    
