'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class DatosPago(BaseModel):
    '''
	`user_id` bigint NOT NULL,
	`medio` int NOT NULL comment '1 Transfernecia, 2 Cheque, 3 contado',
	`banco_id` bigint NULL,    
	`tipo_cuenta` int NULL comment '1 Corriente 2 Ahorro',     
    '''
    user_id : int = Field(ge=1, le=20000)
    medio : int 
    banco_id : int 
    tipo_cuenta : int
    numero_cuenta : str = Field(min_length=0, max_length=100)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "medio":1,
                    "banco_id":1,
                    "tipo_cuenta":1,
                    "numero_cuenta":""
                }
            ]
        }
    }    
