# Schema de datos de Usuario
# se usa como interfaz de captura de Datos para luego
# pasar su contenido a el modelo de Usuario
from pydantic import BaseModel, Field
from typing import  Optional, List
from datetime import date, datetime

#clase que representa a un usuario en el sistema
class PreUser2(BaseModel):
    documento: str = Field (min_length=3, max_length=100)
    nombres : str = Field (min_length=2, max_length=100)
    apellidos :str   = Field (min_length=2, max_length=100)
    correo :str   = Field (min_length=3, max_length=250)
    nacionalidad : int
    genero : int
    fechaNacimiento : date
    estadoCivil : int
    region : int
    localidad : int
    direccion : str = Field (min_length=0, max_length=250)
    telefonoCelular : str = Field (min_length=0, max_length=20)
    telefonoLocal : str = Field (min_length=0, max_length=20)


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documento": "19176716-0",
                    "nombres": "CLAUDIA ESTEFANIA",
                    "apellidos": "OLGUIN",
                    "correo": "valentina.castro@2callcenter.cl",
                    "nacionalidad": 1,
                    "genero": 2,
                    "fechaNacimiento": "1997-01-24",
                    "estadoCivil": 1,
                    "region": 13,
                    "localidad": 13101,
                    "direccion": "Sazie 2496",
                    "telefonoCelular": "930542965",
                    "telefonoLocal": "",
                }
            ]
        }
    }    
