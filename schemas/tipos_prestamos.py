'''
Esquema de datos que define a la tabla Sedes
Created 2024-01
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class TiposPrestamos(BaseModel):
    sociedad_id : int = Field(ge=1, le=1000)
    descripcion : str = Field(min_length=3, max_length=150)
    cuenta : str = Field(min_length=0, max_length=30)
    CCAF : bool
    caja_compensacion_id : int = Field(ge=0, le=1000)

    '''
    sociedad_id = Column (BIGINT, ForeignKey("Sociedad.id", ondelete="RESTRICT", onupdate="CASCADE"),nullable=False)    
    descripcion = Column(VARCHAR(150), nullable=False)
    cuenta = Column(VARCHAR(30), nullable=True)     
    CCAF = Column (int, nullable=False)    
    caja_compensacion_id = Column (BIGINT, nullable=True)     
    '''

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sociedad_id": 1,
                    "descripcion":"Empresa",
                    "cuenta": "11080003",
                    "CCAF": True,
                    "caja_compensacion_id": 0 
                }
            ]
        }
    }    
