'''
Esquema de datos que define a la tabla AFP
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un usuario en el sistema
class AFP(BaseModel):
    id : int,
    codigo_previred : str = Field(min_length=3, max_length=50),
    nombre  : str = Field(min_length=3, max_length=100)  ,
    cotizacion : float ,
    cuenta_AFP : str = Field(min_length=0, max_length=50) ,
    sis : float ,   
    cuenta_sis_cred : str = Field(min_length=0, max_length=20),   
    cuenta_ahorro_AFP_cuenta2 : str = Field(min_length=0, max_length=150),
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=20)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo": "001",
                    "nombre":"BANCO CHILE Y EDWARDS",
                    "nomina": 1
                }
            ]
        }
    }    
