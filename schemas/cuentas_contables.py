'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class CuentasContable(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    acct_code : str = Field(min_length=3, max_length=20)
    acct_name : str = Field(min_length=3, max_length=100)
    finance : str = Field(min_length=1, max_length=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "acct_code":"11010001",
                    "acct_name":"Caja",                    
                    "finance":"Y"                    
                }
            ]
        }
    }    
