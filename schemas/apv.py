'''
Esquema de datos que define a la tabla APVInstituciones
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un usuario en el sistema
class APVInstituciones(BaseModel):
    id : int = Field (min=1, max=2000) 
    nombre  : str = Field(min_length=3, max_length=300)  
    nombre_largo  : str = Field(min_length=3, max_length=250)      
    cuenta_contable : str = Field(min_length=0, max_length=100)     
    codigo_externo : str = Field(min_length=0, max_length=50)     
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id" : 5,
                    "nombre"  : "Habitat",
                    "nombre_largo"  : "Habitat",
                    "cuenta_contable": '21050001',
                    "codigo_externo": '005'
                }
            ]
        }
    }    
