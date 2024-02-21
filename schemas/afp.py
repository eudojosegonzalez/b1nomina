'''
Esquema de datos que define a la tabla AFP
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un usuario en el sistema
class AFP(BaseModel):
    id : int = Field (min=1, max=2000) 
    codigo_previred : str = Field(min_length=3, max_length=50) 
    nombre  : str = Field(min_length=3, max_length=100)  
    cotizacion : float = Field (min=0, max=20000)
    cuenta_AFP : str = Field(min_length=0, max_length=50) 
    sis : float   = Field (min=0, max=20000) 
    cuenta_sis_cred : str = Field(min_length=0, max_length=20)  
    cuenta_ahorro_AFP_cuenta2 : str = Field(min_length=0, max_length=150)
    codigo_direccion_trabajo: str = Field(min_length=0, max_length=20)  

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo_previred" : "001",
                    "nombre"  : "AFP Prueba",
                   "cotizacion" : 0,
                    "cuenta_AFP" : "0001" ,
                    "sis" : 0,
                    "cuenta_sis_cred" : "",   
                    "cuenta_ahorro_AFP_cuenta2" : "",
                   "codigo_direccion_trabajo": ""  
                }
            ]
        }
    }    
