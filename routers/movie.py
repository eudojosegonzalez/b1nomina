from fastapi import APIRouter
from fastapi import Path,Query, Depends
from fastapi.responses import  JSONResponse
#from pydantic import BaseModel,Field
#from typing import  Optional, List
from typing import  List
# dependencia que coinvierte los objketos tipo Bd a json
from fastapi.encoders import jsonable_encoder
from utils.jwt_managr import create_token,validate_token
# importamos los servicio 
from services.movie import MovieService

# importamos las clases desde 
# la configuracion de la base de datos
from config.database import Session
# esto importa la tabla desde la definicione de modelos
from models.movie import Movie as MovieModel
# importamos el modelo de la tabla desde el directorio schemas
from schemas.movie import Movie


#from middleware.error_handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer
movie_router = APIRouter()


# esta ruta esta autenticada, lo mismo se logra agregando la dependencia  Depends (JWTBearer())
# que tipo de respuesta se obtendrá del metodo response_model= esto puede ser una lista, un registro etc
# tags etiqueta para mostrar en la Docs
# /movies ruta o endpoints de la aplicacion
# que se devolverá return JSONResponse(content=jsonable_encoder(result))
@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies()->list[Movie]:
    db = Session()
    # sin servicio
    #result=db.query(MovieModel).all()
    #con servicios
    result = MovieService(db).get_movies()
    # debemnos convertir los objetos tipo BD a Json
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

# esto es la busqueda por id de la pelicula
@movie_router.get('/movies/{id}',tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1, le=2000)):
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id==id).first()
    # metodo de busqueda sin servicio
    #result = db.query(MovieModel).filter(MovieModel.id==id).first()
    #metodo de busqueda con servicio
    result = MovieService(db).get_movie(id)
    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})
    #new_list = list(filter(lambda item: item['id'] == id, movies))
    '''for item in movies:
        if item['id']==str(id):
            return item '''
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#esto es la busqueda por categoria
#en este caso el parametro se coloca en la función, no en la ruta
# es un parámetro query
# cada parametro debe ser un elemento en la función
@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str = Query(min_length=5,max_length=50)):
    db = Session()
    # sin servicio
    #result = db.query(MovieModel).filter(MovieModel.category==category).all()
    # con servicio
    result = MovieService(db).get_movie_category(category)
    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})
    #data = [ item for item in movies if item['category']== category]
    '''    for item in movies:
        if item['category']==category:
            return item '''
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

# esta funcion permite crear una pelicula
# se añade a cada parametro el tag body para que no lo tome como un parametro query sino como parte 
# de la peticion 
@movie_router.post ('/movies/',tags=['movies'], response_model=dict)
#def create_movies(id:int = Body(), title:str = Body() , overview:str = Body(), year:int = Body(), rating: float = Body(),category:str = Body()):
def create_movies(movie : Movie)->dict:
    db=Session()
    # hay dos formas de ingresar la data la primera es 
    # primera forma
    #MovieModel(title=movie.title, year=movie.year, rating=movie.rating, category=movie.category)
    #Segunda Forma
    # new_movie=MovieModel(**movie.dict())
    #creamos el nuevo registro en la tabla
    # db.add(new_movie)
    #confirmamos los cambios
    # db.commit()
    #movies.movie_routerend(movie)
    #return movies[-1]
    #usando un servicio
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message":"Success"})


@movie_router.put('/movies/{id}',tags=['movies'], response_model=dict)
#def update_movie(id:int,title:str = Body() , overview:str = Body(), year:int = Body(), rating: float = Body(),category:str = Body()):
def update_movie(id:int, movie: Movie)->dict:
    db = Session()
    # sin servicio
    '''result=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})

    result.title=movie.title
    result.overview=movie.overview
    result.year=movie.year
    result.rating=movie.rating
    result.category=movie.category
    
    #conformamos los cambios
    db.commit()'''

    '''    for item in movies:
    if item['id']==id:
        item['title']=movie.title     
        item['overview']=movie.overview
        item['year']=movie.year
        item['rating']=movie.rating
        item['category']=movie.category

        #return item'''    

    #con servicio
    result=MovieService(db).get_movie(id)

    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})

    result=MovieService(db).update_movie(id,movie)
    return JSONResponse(content={"message":"Success"})

@movie_router.delete ('/movies/{id}',tags=['movies'], response_model=dict)
def delete_movie(id:int)->dict:
    db = Session()
    # sin servicio
    '''result=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})    
            for item in movies:
        if item['id']==id:
            movies.remove(item)
            return JSONResponse(content={"message":"Success"})
    db.delete(result)
    db.commit()'''

    # con servicio
    result=MovieService(db).get_movie(id)    
    if not result:
        return  JSONResponse(status_code=404, content={"message":"No encontrado"})

    result=MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message":"Se eliminó de forma exitosa"})