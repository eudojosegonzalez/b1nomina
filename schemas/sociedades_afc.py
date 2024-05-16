'''
Esquema de datos que define a la tabla Sociedades AFC
Created 2024-05
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class SociedadesAFC(BaseModel):
    sociedad_id : int
    afc_empresa : float
    afc_empleado : float
    afc_plazo_fijo : float
    afc_antiguedad : float
    tope_seguro_afc : float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id" : 1,
                    "afc_empresa" : 1.00,
                    "afc_empleado" : 1.00,
                    "afc_plazo_fijo" : 1.00,
                    "afc_antiguedad" : 1.00,
                    "tope_seguro_afc" : 1.00
                }
            ]
        }
    }    
