# Schema de datos de  Sede Departamento Grupo
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List

#clase que representa a un modelo Sede Departamento Grupo en el sistema
class SDG(BaseModel):
   sede_id : int = Field (ge=0, lt= 20000)
   departamento_id: int = Field (ge=0, lt= 20000)
   grupo_id : int = Field (ge=0, lt= 20000)

   model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sede_id": 1,
                    "departamento_id": 1,
                    "grupo_id": 1
                }
            ]
        }
    }    
