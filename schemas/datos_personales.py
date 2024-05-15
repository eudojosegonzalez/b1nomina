# Schema de datos de Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa a un usuario en el sistema
class DatosPersonales(BaseModel):
    rut: str = Field (min_length=3, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    fecha_nacimiento : date
    sexo_id : int  = Field (ge=1, le= 2)
    estado_civil_id : int  = Field (ge=1, le= 5)
    nacionalidad_id : int   = Field (ge=1, le= 200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rut": "1-9",                 
                    "nombres": "Pedro ",
                    "apellido_paterno" : "Perez",
                    "fecha_nacimiento": "1990-01-01",
                    "sexo_id":"1",
                    "estado_civil_id":"1",
                    "nacionalidad_id":"1"                
                }
            ]
        }
    }    
