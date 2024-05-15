'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class Configuraciones(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    categoria_id : int = Field(ge=1, le=1000)
    nombre : str = Field(min_length=3, max_length=200)    
    valor : float
    detalle : str = Field(min_length=0, max_length=500)   
    cuenta : str = Field(min_length=0, max_length=50) 
    ocultar : int
    tipo_validacion : str = Field(min_length=0, max_length=30)
    orden : int


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'sociedad_id': 1,  
                    'categoria_id': 1,                    
                    'nombre': 'Sueldo Minimo ($)',
                    'valor': 445000.00,                    
                    'detalle': '',
                    'cuenta': '',                    
                    'ocultar': 0,
                    'tipo_validacion':'Numerico',
                    'orden': 1
               }
            ]
        }
    }    
