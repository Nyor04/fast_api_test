from fastapi import Depends, Path, Request, Response, FastAPI, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
 
from jwt_manager import jwt_generator, jwt_validator
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re #regular expresions gods.
import ipdb

from models_config.db_manager import engine, Session, Base, sqlite_file_name, base_dir
from models.movie_model import Movie as MovieModel
from sqlalchemy import select, update, delete, and_ , or_
from os import path


app = FastAPI(
    title="The Anything API",
    version="1.0",
    description="API para interactuar con una base de datos que contiene informacion sobre muchas cosas, los endopoints de un tema especifico estaran agrupados util para comprender el funcionamiento del framework Fast API.",
)  # crear una instancia de la clase FastAPI es el segundo paso para poder usar el framework.

if path.exists(path.join(base_dir,sqlite_file_name)):
    pass #si la DB existe, pues no hagas mas nada mijo.
else:
    Base.metadata.create_all(bind=engine) #creacion de la DB descrita en models.movie_db

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


#Template for interactic with db
#  tsession = Session()
#     try:
#         pass
#     except:
#         pass
#     finally:
#         tsession.close()

@app.get(
    "/movies",
    tags=["Movies"],
    description='retorna todas las peliculas existentes en "movie_list"',
    response_model=List[Movie]
)
def get_movies() -> List[Movie]:
    tsession = Session()
    try:
        query = tsession.query(MovieModel).all()
        movie_list = [movie.__dict__ for movie in query]
    except:
        return JSONResponse(content={'message':'error during transaction: LISTING MOVIES'})
    finally:
        tsession.close()
        return JSONResponse(status_code=200, content=jsonable_encoder(movie_list))


@app.get(
    "/movies/{id}",
    tags=["Movies"],
    description="retorna una pelicula especifica basandose en su ID utilizando parametros de ruta, si la respuesta es una lista vacia, significa que no existe una pelicula con el id suministrado",
    response_model=List[Movie]
)
def get_movies_by_id(id: int = Path(ge=1)) -> Movie:
    tsession = Session()
    try:
        query = select(MovieModel).filter(MovieModel.id == id)
        result = tsession.execute(query).scalars().all()
    except:
        tsession.rollback()
        return JSONResponse(content={'message':'error during transaction: GETTING MOVIE BY ID'})
    finally:
        tsession.close() 
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    
@app.get(
    "/movies/",
    tags=["Movies"],
    description="retorna una o mas  peliculas basandose en los atributos 'category' y 'year', los cuales son filtros.",
    response_model=List[Movie]
)
def get_movies_by_category_and_year(category: str, year: int) -> List[Movie]:
    tsession = Session()
    try:
        query = select(MovieModel).filter(and_(MovieModel.category == category, MovieModel.year == year))
        result = tsession.execute(query).scalars().all()
    except:
        tsession.rollback()
        return JSONResponse(content={'message':'error during transaction: GETTING MOVIE BY CATEGORY AND YEAR'})
    finally:
        tsession.close()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

"""
la diferencia entre parametros de rutas y parametros de query es que en parametros de ruta el identificador se encuentra dentro de la url
y la funcion que se ejecuta en el endpoint recibe como argumento el parametro indicado en la url. ejemplo

/etc/etc/1 <-- url
get_movies_by_id(1)


En los parametros de querys en otro lado, los argumentos se suministran en la url a forma de variables (nombre X despues de un ?, ex: "?categoria=xxxx")
esto se programa pasandole parametros a la funcion que ejecuta el endpoint pero no se definen estos parametros en el decorador del endpoint.
"""

#post Request para agregar pelicula a la lista
@app.post(
    "/movies",
    tags=["Movies"],
    description="agrega una pelicula a la lista de movie_list"
)
def post_movies(movie:Movie):
    tsession = Session()
    try:
        new_movie = MovieModel(**movie.model_dump())
        tsession.add(new_movie)
        tsession.commit()
    except:
        tsession.rollback()
        return JSONResponse(content={'message':'error during transaction: ADDING MOVIE'})
    finally:
        tsession.close()
        return JSONResponse(content={'message':'Movie Added!'})



@app.put(
    "/movies/{id}",
    tags=["Movies"],
    description="actualiza una pelicula a la lista de movie_list"
)
def put_movies(id: int, movie:Movie) :
    tsession = Session()
    try:
        query = update(MovieModel).where(MovieModel.id == id).values(**movie.model_dump())
        tsession.execute(query)
        tsession.commit()
        return JSONResponse(content={'message':'Movie Info Updated'})

    except:
        tsession.rollback()
        return JSONResponse(content={'message':'error during transaction: UPDATING MOVIE'})
    finally:
        tsession.close()
    
    '''
    investigar porque esta funcion esta generando rollback y no aplica los cambios a la base de datos.
    '''

@app.delete(
    "/movies/{id}",
    tags=["Movies"],
    description="elimina una pelicula a la lista de movie_list"
)
def delete_movies(id: int):
    tsession = Session()
    try:
        query = delete(MovieModel).where(MovieModel.id == id)
        tsession.execute(query)
        tsession.commit()

    except:
        tsession.rollback()
        return JSONResponse(content={'message':'error during transaction: DELETING A MOVIE'})
    finally:
        tsession.close()
        return JSONResponse(content={'message':'Movie Deleted'}, status_code=204)





# @app.get("/",tags=["generic"])  # cuando en nuestra aplicacion se haga un get request hacia la URL que indiquemos en el argumento del decorador
# def read_root():  # <--- se ejecutara esta funcion
#     return {"message": "hello World!"}  # para este ejemplo, deberia retornar un Hello world.


# # interaccion con la API: se puede tener rutas dinamicas usando placeholders, estos van en llaves. los valores puestos aca son dinamicos como Pks.
# @app.get("/items/{item_id}",tags=["generic"])  # <-- estos place holders se les conoce como parametros de ruta.
# def read_item(item_id: int,):  # <-- el parametro de ruta tomado de la url pasa como argumento a la funcion a ejecutar cuando se llama la url (en este caso /items/{item_id})
#     return {"item_id": item_id}  # retornando el json como de costumbre.


# # parametros de busqueda.
# @app.get("/items/",tags=["generic"])
# def read_item(skip: int = 0, limit: int = 10):  # <--- declarar parametros en la funcion a ejecutar cuando se hace un get request a la URL se le conocen como parametros de busqueda. es como hacer querys en la URL usando "?" como indicador de un parametro para luego darle un valor.
#     return {"skip": skip, "limit": limit}

# """
# Ejemplo :http://127.0.0.1:8000/items/?skip=10&limit=20, recibirás:


# {
#     "skip": 10,
#     "limit": 20
# }
# Ejemplo :http://127.0.0.1:8000/items/, en teoria recibes recibirás:


# {
#     "skip": 0,
#     "limit": 10
# }

# debido a que son valores por defecto de estos parametros.
# """


# #
# @app.get("/custom_response/{uname}",description="para dar respuestas personalizadas se debe importar la clase response de la libreria de fastapi",tags=["generic"])
# def get_custom_response(uname: str):
#     message = f"Hola {uname}, esta es una respuesta personalizada de FAST API."
#     return Response(content=message, media_type="text/plain")

# """
# recibimos un string en el parametro {uname}, el cual debe ser uns tring para luego insertar dicho string en un
# mensaje de respuesta personalizado, favor notar que se debe indicar el media type y pasar el atributo content, el charset por defecto es utf-8.

# """


#endpoints relacionados con users creados apartir de aqui.

email_format = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
user_list = [
    {    
        "id": 1,
        "username": "burena",
        "email": "test@dev.com",
        "is_active": True,
        "address": [
            {
            "city": "si",
            "state": "alli",
            "country": "nunca jamas"
            }
        ],
        "roles": [
            "user"
        ]
    }
    
]

class Address(BaseModel):
    city:str
    state:str
    country:str

class UpdateRoleAtrribute(BaseModel):
    roles:list[str]

class User(BaseModel):
    id:int
    username:str
    email:str = 'test@dev.com'
    is_active:bool = True
    address:list[Address]
    roles:list

  

    @field_validator("email")
    def email_validator(cls, value): 
        if not isinstance(value, str):  
            raise ValueError("Email must be a string.")
        if not re.match(email_format, value):
            raise ValueError("Invalid email format.")
        return value
    
    @field_validator('roles')
    def roles_validator(cls,value):
        if not value:
            raise ValueError("User must have at least 1 rol assigned.")
        return value

class LoginData(BaseModel):
    email:str
    password:str

    @field_validator("email")
    def email_validator(cls, value): 
        if not isinstance(value, str):  
            raise ValueError("Email must be a string.")
        if not re.match(email_format, value):
            raise ValueError("Invalid email format.")
        return value

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data = jwt_validator(auth.credentials)
        if data['email'] != "mock@email.com" or data["password"] != "mockpassword":
            raise HTTPException(status_code=401,detail="Credenciales invalidas")


@app.get("/users", tags=['Users'], dependencies=[Depends(JWTBearer())])
def get_users():
    return user_list

@app.get("/users/{id}", tags=['Users'])
def get_users(id:int):
    return user_list[id]

@app.post("/users", tags=['Users'])
def create_users(user:User):
    if any(product.id == user.id for product in user_list):
        return {'message':f"User id must be unique!, id {user.id} already in use"}
    user_list.append(user)
    return {'message':'User added', 'user_object':user_list}

@app.put("/users/{id}", tags=['Users'])
def update_users(id:int, user:User):
    user_index = next((index for index, value in enumerate(user_list) if value.id == id))
    if user_index == None:
        raise HTTPException(status_code=404, detail="User Does Not Exist")
    else:
        user_list[user_index] = user
        return {'message':'user updated', 'user_object':user_list[user_index]}

@app.patch("/users/{id}/roles", tags=['Users'],description="este endopoint acutaliza el atributo roles de los objetos usuarios.")
def update_users_role(id:int, roles:UpdateRoleAtrribute ):
    user_index = next((index for index, value in enumerate(user_list) if value['id'] == id))
    if user_index == None:
        raise HTTPException(status_code=404, detail="User Does Not Exist")
    else:
        user_list[user_index]['roles']=roles.roles
        return {'message':"Roles attribute updated", "updated_object":user_list[user_index]}
    
@app.post("/login", tags=['auth'])
def login(user:LoginData):
    if user.email == "mock@email.com" and user.password == "mockpassword":
        token:str = jwt_generator(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    else:
        message = {"message":"Auth failed, check your credentials"}
        return JSONResponse(content=message)