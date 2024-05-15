'''
Esquema de datos que define a la tabla Estatus Inscripcion de Usuarios
Created 2024-04
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class EstatusInscripcionPago(BaseModel):
    user_id : int = Field(ge=1, le=2000)
  
    # --datos de pago -----------------------------------------# --
    medio : int = Field (ge=0,le=1)    
    banco : int = Field (ge=0,le=1)     
    tipo_cuenta : int = Field (ge=0,le=1)    
    numero : int = Field (ge=0,le=1)     
 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "medio":0,   
                    "banco":0,
                    "tipo_cuenta":0,   
                    "numero":0
                }
            ]
        }
    }    
