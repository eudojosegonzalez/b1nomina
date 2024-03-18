'''
Esquema de datos que define a la tabla Tramos de Impuesto Único
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class TramosImpuestoUnico(BaseModel):
    tramo : str = Field(min_length=3, max_length=250)
    desde :  float
    hasta : float
    factor : float
    rebaja : float
    
    #'Tramo 1','0.000','13.500','0.000','0.000'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tramo":"Tramo 1",
                    "desde" : 0.00,
                    "hasta" : 13.50,
                    "factor": 0.00,
                    "rebaja": 0.00
                }
            ]
        }
    }    
