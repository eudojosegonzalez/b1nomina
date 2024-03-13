'''
Esquema de datos que define a la Tramos de Asignacion Familiar
Created 2024-02
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class TramosAsignacionFamiliar(BaseModel):
    tramo : str = Field(min_length=3, max_length=250)
    desde :  float
    hasta : float
    valor_carga : float
    
    #'Tramo 1','0.000','13.500','0.000','0.000'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tramo":"Tramo 1",
                    "desde" : 0.00,
                    "hasta" : 13.50,
                    "valor_carga": 0.00,
                }
            ]
        }
    }    
