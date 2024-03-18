'''
Esquema de datos que define a la tabla Ubicacion del usuario
Created 2024-03
'''
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa la localización geográfica del usuario en el sistema
class UbicacionUserMassive(BaseModel):
    user_id: int = Field (ge=1, lt=20000)
    region_id: int = Field (ge=1, lt=20000)
    comuna_id: int = Field (ge=1, lt=20000)
    direccion: str = Field (min_length= 0, max_length= 250)
  
 
