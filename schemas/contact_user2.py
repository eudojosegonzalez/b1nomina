'''
Esquema de datos que define a la tabla Contacto del usuario
Created 2024-03
'''
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa los datos de contacto del  usuario en el sistema
class ContactUserMassive(BaseModel):
    user_id: int = Field (ge=1,lt=20000)
    email : Optional[str]  = Field (min_length=0, max_length=250)
    fijo : Optional[str]  = Field (min_length=0, max_length=20) 
    movil : Optional[str]  = Field (min_length=0, max_length=20)
