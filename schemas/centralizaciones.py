'''
Esquema de datos que define a la tabla Centralizacion
Created 2024-01
'''
from pydantic import BaseModel, Field


#clase que representa a un Banco en el sistema
class Centralizaciones(BaseModel):
    sociedad_id : int = Field(ge=1, le=2000)
    usa_centros_costos : int = Field(ge=0, le=1)
    cuenta_anticipo : str =Field (min_length=0, max_length=50)
    cuenta_bonos_feriado : str =Field (min_length=0, max_length=50)
    cuenta_honorarios : str =Field (min_length=0, max_length=50)
    cuenta_prestamos_solidarios : str =Field (min_length=0, max_length=50)
    prestamo_solidario_imponible  : int = Field(ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id" : 1,
                    "usa_centros_costos" : 1,
                    "cuenta_anticipo" : "",
                    "cuenta_bonos_feriado" : "",
                    "cuenta_honorarios" : "",
                    "cuenta_prestamos_solidarios" : "",
                    "prestamo_solidario_imponible"  : 1
                }
            ]
        }
    }    
