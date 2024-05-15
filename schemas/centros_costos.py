'''
Esquema de datos que define a la tabla Centros de Costos
Created 2024-03
'''
from pydantic import BaseModel, Field


#clase que representa a un Banco en el sistema
class CentrosDeCostos(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    codigo_sap : str = Field (min_length=0, max_length=50)
    centro_costo : str = Field (min_length=0, max_length=200)
    dimension_id : int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id" : 1,
                    "codigo_sap" : "",
                    "centro_costo" : "",
                    "dimension_id" : 1
                }
            ]
        }
    }    
