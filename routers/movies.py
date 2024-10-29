from fastapi import APIRouter

from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
 
from services.movie import MovieService

from pydantic import BaseModel, Field
from typing import List, Optional


from models_config.db_manager import Session



movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2024)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }



@movie_router.get(
    "/movies",
    tags=["Movies"],
    description='retorna todas las peliculas existentes en "movie_list"',
    response_model=List[Movie]
)
def get_movies() -> List[Movie]:
    tsession = Session()
    try:
        result = MovieService(tsession).get_movies()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close()


@movie_router.get(
    "/movies/{id}",
    tags=["Movies"],
    description="retorna una pelicula especifica basandose en su ID utilizando parametros de ruta, si la respuesta es una lista vacia, significa que no existe una pelicula con el id suministrado",
    response_model=List[Movie]
)
def get_movies_by_id(id: int = Path(ge=1)) -> Movie:
    tsession = Session()
    try:
        result = MovieService(tsession).get_movie(id)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        tsession.rollback()
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close() 
    
@movie_router.get(
    "/movies/",
    tags=["Movies"],
    description="retorna una o mas  peliculas basandose en los atributos 'category' y 'year', los cuales son filtros.",
    response_model=List[Movie]
)
def get_movies_by_category_and_year(category: str, year: int) -> List[Movie]:
    tsession = Session()
    try:
       
        result = MovieService(tsession).get_movies_by_category_and_year(category=category,year=year)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        tsession.rollback()
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close()

@movie_router.post(
    "/movies",
    tags=["Movies"],
    description="agrega una pelicula a la lista de movie_list"
)
def post_movies(movie:Movie):
    tsession = Session()
    try:
        MovieService(tsession).post_movie(**movie)
        return JSONResponse(content={'message':'Movie Added!'})
    except Exception as e:
        tsession.rollback()
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close()



@movie_router.put(
    "/movies/{id}",
    tags=["Movies"],
    description="actualiza una pelicula a la lista de movie_list"
)
def put_movies(id: int, movie:Movie) :
    tsession = Session()
    try:
        MovieService(tsession).put_movie(id, **movie)
        return JSONResponse(content={'message':'Movie Info Updated'})

    except Exception as e:
        tsession.rollback()
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close()
    
 

@movie_router.delete(
    "/movies/{id}",
    tags=["Movies"],
    description="elimina una pelicula a la lista de movie_list"
)
def delete_movies(id: int):
    tsession = Session()
    try:
        MovieService(tsession).delete_movie(id)
        return JSONResponse(content={'message':'Movie Deleted'}, status_code=204)
    except Exception as e:
        tsession.rollback()
        return JSONResponse(content={'message':f'error during transaction:{str(e)}'})
    finally:
        tsession.close()


