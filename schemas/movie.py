from pydantic import BaseModel,Field
from typing import  Optional, List

#modelo de la tabla
class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field( min_length=5, max_length=15) 
    overview : str     
    year : int = Field(ge=1970,le=2022)
    rating : float =Field(ge=1,le=10)
    category : str = Field( min_length=5, max_length=25) 

    model_config = {
        "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "title": "Mi Pelicula",
                        "overview": "Descripcion de la pelicula",
                        "year": 2022,
                        "rating": 9.9,
                        "category": "Acción"
                    }
                ]
            }
    }