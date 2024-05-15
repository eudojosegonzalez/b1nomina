'''
Esquema de datos que define a la tabla Bancarios de la Sociedad
Created 2024-03
'''
from pydantic import BaseModel, Field


#clase que representa a  alos datos bancarios del usuario en el sistema
class BancarioSociedad(BaseModel):
    sociedad_id: int = Field (ge=1,lt=20000)
    banco_id : int = Field(gr=1, lt=1000)
    numero_cuenta : str = Field (min_length=3, max_length=100)
    codigo_convenio: str = Field (min_length=0, max_length=100)
    giro_empresa : str = Field (min_length=0, max_length=150)
    razon_social  : str = Field (min_length=0, max_length=150)
    ocultar_mail : bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": '1',
                    "banco_id" : '1',
                    "numero_cuenta" : '0102002',
                    "codigo_convenio": '',
                    "giro_empresa" : '',
                    "razon_social"  : '',
                    "ocultar_mail" : True
                }
            ]
        }
    }    
