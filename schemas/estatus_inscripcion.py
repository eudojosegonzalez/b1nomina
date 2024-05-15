'''
Esquema de datos que define a la tabla Estatus Inscripcion de Usuarios
Created 2024-04
'''
from pydantic import BaseModel, Field

#clase que representa a una sociedad en el sistema
class EstatusInscripcion(BaseModel):
    user_id : int = Field(ge=1, le=2000)
    rut : int = Field (ge=0,le=1) 
    nombre : int = Field (ge=0,le=1)     
    apellido : int = Field (ge=0,le=1)    
    nacionalidad : int = Field (ge=0,le=1)     
    sexo : int = Field (ge=0,le=1)    
    fecha_nac : int = Field (ge=0,le=1)     
    estado_civil : int = Field (ge=0,le=1)    
    # --ubicacion ----------------
    region : int = Field (ge=0,le=1)    
    comuna : int = Field (ge=0,le=1)     
    direccion : int = Field (ge=0,le=1)    
    # --contacto ------------------------------------
    telefono : int = Field (ge=0,le=1)     
    email : int = Field (ge=0,le=1)     
    # --laborales ---------------------------------# --
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
    # --datos de pago -----------------------------------------# --
    medio : int = Field (ge=0,le=1)    
    banco : int = Field (ge=0,le=1)     
    tipo_cuenta : int = Field (ge=0,le=1)    
    numero : int = Field (ge=0,le=1)     
    # --archivos necesarios --------------------------------------------# --   
    foto : int = Field (ge=0,le=1)    
    cv : int = Field (ge=0,le=1)     
    contrato : int = Field (ge=0,le=1)      
 

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id" : 1,
                    "rut":0,
                    "nombre":0,
                    "apellido":0,   
                    "nacionalidad":0,
                    "sexo":0,   
                    "fecha_nac":0,
                    "estado_civil":0,   
                    "region":0,   
                    "comuna":0,
                    "direccion":0,   
                    "telefono":0,
                    "email":0,
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
                    "nivel_estudio":0,
                    "medio":0,   
                    "banco":0,
                    "tipo_cuenta":0,   
                    "numero":0,
                    "foto":0, 
                    "cv":0,
                    "contrato":0
                }
            ]
        }
    }    
