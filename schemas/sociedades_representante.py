'''
Esquema de datos que define a la tabla Sociedades
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class SociedadesRepresentante(BaseModel):
    responsable : str = Field(min_length=0, max_length=150)
    rut_responsable : str = Field(min_length=3, max_length=100) 
    email_responsable : str = Field(min_length=0, max_length=250)    
    telefono_responsable : str = Field(min_length=0, max_length=20)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'responsable':'',
                    'rut_responsable':'',
                    'email_responsable':'',
                    'telefono_responsable':''
                }
            ]
        }
    }    
