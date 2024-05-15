'''
Esquema de datos que define a la Tramos de Asignacion Familiar
Created 2024-02
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class TramosAsignacionFamiliar(BaseModel):
    tramo : str = Field(min_length=1, max_length=250)
    desde :  float
    hasta : float
    valor_carga : float
    
    #'Tramo 1','0.000','13.500','0.000','0.000'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tramo":"A",
                    "desde" : 0.00,
                    "hasta" : 315841.000,
                    "valor_carga": 12364,
                }
            ]
        }
    }    
