from pydantic import BaseModel, Field
from datetime import date

class User(BaseModel):
    id : int = Field (ge=1, lt= 2000)
    rut: str = Field (min_length=8, max_length=100)
    rut_provisorio : str = Field (min_length=8, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellido_paterno :str   = Field (min_length=2, max_length=100)
    apellido_materno : str = Field (min_length=2, max_length=100)
    fecha_nacimiento : date
    sexo_id : int  = Field (ge=1, le= 2)
    estado_civil_id : int  = Field (ge=1, le= 5)
    nacionalidad_id : int   = Field (ge=1, le= 200)
    username : str  = Field (min_length=8, max_length=200)   
	password : str = Field (min_length=8, max_length=200)


class Credenciales(BaseModel):
    username : str  = Field (min_length=8, max_length=200)   
	password : str = Field (min_length=8, max_length=200)