'''
Esquema de datos que define a la tabla Estatus Inscripcion de Usuarios
Created 2024-04
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class EstatusInscripcionLaboral(BaseModel):
    user_id : int = Field(ge=1, le=2000)
    tipo_contrato : int = Field (ge=0,le=1)    
    termino : int = Field (ge=0,le=1)     
    fecha_contratacion : int = Field (ge=0,le=1)    
    salario_base : int = Field (ge=0,le=1)     
    unidad_sueldo : int = Field (ge=0,le=1)    
    monto_sueldo : int = Field (ge=0,le=1)     
    sociedad : int = Field (ge=0,le=1)        
    sede : int = Field (ge=0,le=1)    
    departamento : int = Field (ge=0,le=1)    
    cargo : int = Field (ge=0,le=1)     
    grupo : int = Field (ge=0,le=1)    
    modalidad : int = Field (ge=0,le=1)     
    dias_descanso : int = Field (ge=0,le=1) 
    nivel_estudio : int = Field (ge=0,le=1)     
 
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "tipo_contrato":0,   
                    "termino":0,
                    "fecha_contratacion":0,   
                    "salario_base":0,
                    "unidad_sueldo":0,   
                    "monto_sueldo":0,
                    "sociedad":0,   
                    "sede":0,   
                    "departamento":0,   
                    "cargo":0,
                    "grupo":0,   
                    "modalidad":0,
                    "dias_descanso":0,
                    "nivel_estudio":0
                }
            ]
        }
    }    
