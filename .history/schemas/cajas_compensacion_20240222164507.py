'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class CajasCompensacion(BaseModel):
    nombre : str = Field(min_length=3, max_length=200)
    codigo_externo : str = Field(min_length=2, max_length=50)
    cuenta_contable : str = Field(min_length=2, max_length=50)
    codigo_direccion_trabajo : str = Field(min_length=0, max_length=10)

    '''
	`nombre` VARCHAR(200) NOT NULL,
	`codigo_externo` VARCHAR(50) NOT NULL,
	`cuenta_contable` VARCHAR(50) NOT NULL,
	`codigo_direccion_trabajo` VARCHAR(10) NULL,
    '''

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre":"Los Andes",
                    "codigo_externo":"01",
                    "cuenta_contable":"21050003",
                    "codigo_direccion_trabajo":"1",
                }
            ]
        }
    }    
