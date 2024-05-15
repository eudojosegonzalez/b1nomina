'''
Esquema de datos que define a la tabla Configuraciones de Remuneraciones
Created 2024-05
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class ConfRemuneraciones(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    sueldo_minimo : float 
    gratificacion_minimo: float
    tope_gratificacion : float
    dias_vacaciones: int
    horas_legales : int
    retencion_honorarios : float
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'sociedad_id': 1,  
                    'sueldo_minimo' : 450000.00,
                    'gratificacion_minimo': 1.0,
                    'tope_gratificacion' : 5.0
                    'dias_vacaciones': 15,
                    'horas_legales' : 8,
                    'retencion_honorarios' : 0
               }
            ]
        }
    }    
