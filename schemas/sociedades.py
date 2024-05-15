'''
Esquema de datos que define a la tabla Sociedades
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Sociedades(BaseModel):
    rut : str = Field(min_length=3, max_length=100)
    nombre : str = Field(min_length=3, max_length=250)
    direccion : str = Field(min_length=3, max_length=500)
    region_id : int = Field(ge=1, le=1000)
    comuna_id : int = Field(ge=1, le=1000)
    ciudad : str = Field(min_length=3, max_length=250)
    icono : str = Field(min_length=3, max_length=250)
    email : str = Field(min_length=0, max_length=250)
    responsable : str = Field(min_length=0, max_length=150)
    rut_responsable : str = Field(min_length=3, max_length=100) 
    email_responsable : str = Field(min_length=0, max_length=250)    
    telefono_responsable : str = Field(min_length=0, max_length=20)
    banco_id : int = Field(ge=0, le=1000)
    numero_cuenta : str = Field(min_length=0, max_length=100)
    ocultar_email : int =Field (ge=0, le=1)
    codigo_convenio : str = Field(min_length=0, max_length=100)
    giro_empresa : str = Field(min_length=0, max_length=150)
    razon_social : str = Field(min_length=0, max_length=150) 
    mutual_id : int = Field(ge=1, le=1000)
    porcentaje : float 
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "rut": "RutDemo",
                    "nombre":"Demo",
                    "direccion": "Direccion Demo",
                    "region_id": 1,
                    "comuna_id": 1101,
                    "ciudad":"Demo ciudad",
                    'icono':'',
                    'email':'',
                    'resposable':'',
                    'rut_responsable':'',
                    'email_responsable':'',
                    'telefono_responsable':'',
                    'banco_id':'0',
                    'numero_cuenta':'',
                    'ocultar_email':'0',
                    'codigo_convenio' : '',
                    'giro_empresa': '',
                    'razon_social': '',
                    'mutual_id' : 1,
                    'porcentaje' : 0
                }
            ]
        }
    }    
