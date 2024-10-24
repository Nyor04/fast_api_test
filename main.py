from fastapi import (
    Response,
    FastAPI,
    Body,
    HTTPException
)  # importar la clase de fastAPI es el primer paso para poder usar el framework.
from typing import Union

app = FastAPI(
    title="Movie Anything API",
    version="1.0",
    description="API para interactuar con una base de datos que contiene informacion sobre muchas cosas, los endopoints de un tema especifico estaran agrupados util para comprender el funcionamiento del framework Fast API.",
)  # crear una instancia de la clase FastAPI es el segundo paso para poder usar el framework.


@app.get("/",tags=["generic"])  # cuando en nuestra aplicacion se haga un get request hacia la URL que indiquemos en el argumento del decorador
def read_root():  # <--- se ejecutara esta funcion
    return {"message": "hello World!"}  # para este ejemplo, deberia retornar un Hello world.


# interaccion con la API: se puede tener rutas dinamicas usando placeholders, estos van en llaves. los valores puestos aca son dinamicos como Pks.
@app.get("/items/{item_id}",tags=["generic"])  # <-- estos place holders se les conoce como parametros de ruta.
def read_item(item_id: int,):  # <-- el parametro de ruta tomado de la url pasa como argumento a la funcion a ejecutar cuando se llama la url (en este caso /items/{item_id})
    return {"item_id": item_id}  # retornando el json como de costumbre.


# parametros de busqueda.
@app.get("/items/",tags=["generic"])
def read_item(skip: int = 0, limit: int = 10):  # <--- declarar parametros en la funcion a ejecutar cuando se hace un get request a la URL se le conocen como parametros de busqueda. es como hacer querys en la URL usando "?" como indicador de un parametro para luego darle un valor.
    return {"skip": skip, "limit": limit}

"""
Ejemplo :http://127.0.0.1:8000/items/?skip=10&limit=20, recibirás:


{
    "skip": 10,
    "limit": 20
}
Ejemplo :http://127.0.0.1:8000/items/, en teoria recibes recibirás:


{
    "skip": 0,
    "limit": 10
}

debido a que son valores por defecto de estos parametros.
"""


#
@app.get("/custom_response/{uname}",description="para dar respuestas personalizadas se debe importar la clase response de la libreria de fastapi",tags=["generic"])
def get_custom_response(uname: str):
    message = f"Hola {uname}, esta es una respuesta personalizada de FAST API."
    return Response(content=message, media_type="text/plain")

"""
recibimos un string en el parametro {uname}, el cual debe ser uns tring para luego insertar dicho string en un
mensaje de respuesta personalizado, favor notar que se debe indicar el media type y pasar el atributo content, el charset por defecto es utf-8.

"""

# lista de diccionarios de peliculas para hacer mocks de retorno hosteada en una DB.
movie_list = [ 
    {
        "id": 1,
        "name": "Inception",
        "description": "A skilled thief is given a chance at redemption if he can successfully perform an inception by planting an idea into someone's mind.",
        "category": ["Science Fiction"],
        "rating": 8.8,
        "cover_url": "https://example.com/inception.jpg",
    },
    {
        "id": 2,
        "name": "The Godfather",
        "description": "The patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "category": ["Crime", "Drama"],
        "rating": 9.2,
        "cover_url": "https://example.com/godfather.jpg",
    },
    {
        "id": 3,
        "name": "The Dark Knight",
        "description": "Batman faces his greatest psychological and physical challenges as he battles the Joker, a criminal mastermind.",
        "category": ["Action", "Crime", "Drama"],
        "rating": 9.0,
        "cover_url": "https://example.com/dark_knight.jpg",
    },
    {
        "id": 4,
        "name": "Pulp Fiction",
        "description": "The lives of two mob hitmen, a boxer, a gangster, and his wife intertwine in four tales of violence and redemption.",
        "category": ["Crime", "Drama"],
        "rating": 8.9,
        "cover_url": "https://example.com/pulp_fiction.jpg",
    },
    {
        "id": 5,
        "name": "The Shawshank Redemption",
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "category": ["Drama"],
        "rating": 9.3,
        "cover_url": "https://example.com/shawshank_redemption.jpg",
    },
    {
        "id": 6,
        "name": "Fight Club",
        "description": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much more.",
        "category": ["Drama"],
        "rating": 8.8,
        "cover_url": "https://example.com/fight_club.jpg",
    },
    {
        "id": 7,
        "name": "Forrest Gump",
        "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
        "category": ["Drama", "Romance"],
        "rating": 8.8,
        "cover_url": "https://example.com/forrest_gump.jpg",
    },
    {
        "id": 8,
        "name": "The Matrix",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "category": ["Science Fiction", "Action"],
        "rating": 8.7,
        "cover_url": "https://example.com/the_matrix.jpg",
    },
    {
        "id": 9,
        "name": "The Lord of the Rings: The Return of the King",
        "description": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
        "category": ["Fantasy", "Adventure"],
        "rating": 9.0,
        "cover_url": "https://example.com/lotr_return_of_the_king.jpg",
    },
    {
        "id": 10,
        "name": "Gladiator",
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "category": ["Action", "Drama"],
        "rating": 8.5,
        "cover_url": "https://example.com/gladiator.jpg",
    },
    {
        "id": 11,
        "name": "Titanic",
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "category": ["Drama", "Romance"],
        "rating": 7.8,
        "cover_url": "https://example.com/titanic.jpg",
    },
    {
        "id": 12,
        "name": "Jurassic Park",
        "description": "During a preview tour, a theme park suffers a major power breakdown that allows its cloned dinosaur exhibits to run amok.",
        "category": ["Adventure", "Science Fiction"],
        "rating": 8.1,
        "cover_url": "https://example.com/jurassic_park.jpg",
    },
    {
        "id": 13,
        "name": "Interstellar",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "category": ["Science Fiction", "Drama"],
        "rating": 8.6,
        "cover_url": "https://example.com/interstellar.jpg",
    },
    {
        "id": 14,
        "name": "The Lion King",
        "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
        "category": ["Animation", "Adventure", "Drama"],
        "rating": 8.5,
        "cover_url": "https://example.com/lion_king.jpg",
    },
    {
        "id": 15,
        "name": "Star Wars: Episode IV - A New Hope",
        "description": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee, and two droids to save the galaxy from the Empire's world-destroying battle station.",
        "category": ["Adventure", "Fantasy", "Science Fiction"],
        "rating": 8.6,
        "cover_url": "https://example.com/star_wars_a_new_hope.jpg",
    },
    {
        "id": 16,
        "name": "The Silence of the Lambs",
        "description": "A young F.B.I. cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer.",
        "category": ["Crime", "Drama", "Thriller"],
        "rating": 8.6,
        "cover_url": "https://example.com/silence_of_the_lambs.jpg",
    },
    {
        "id": 17,
        "name": "The Departed",
        "description": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
        "category": ["Crime", "Drama", "Thriller"],
        "rating": 8.5,
        "cover_url": "https://example.com/the_departed.jpg",
    },
    {
        "id": 18,
        "name": "Schindler's List",
        "description": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
        "category": ["Biography", "Drama", "History"],
        "rating": 9.0,
        "cover_url": "https://example.com/schindlers_list.jpg",
    },
    {
        "id": 19,
        "name": "Avengers: Endgame",
        "description": "After the devastating events of Avengers: Infinity War, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
        "category": ["Action", "Adventure", "Science Fiction"],
        "rating": 8.4,
        "cover_url": "https://example.com/avengers_endgame.jpg",
    },
    {
        "id": 20,
        "name": "Back to the Future",
        "description": "Marty McFly, a 17-year-old high school student, is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his close friend, eccentric scientist Doc Brown.",
        "category": ["Adventure", "Comedy", "Science Fiction"],
        "rating": 8.5,
        "cover_url": "https://example.com/back_to_the_future.jpg",
    },
]

#
@app.get(
    "/movies",
    tags=["Movies"],
    description='retorna todas las peliculas existentes en "movie_list"',
)
def get_movies():
    return movie_list

#
@app.get(
    "/movies/{id}",
    tags=["Movies"],
    description="retorna una pelicula especifica basandose en su ID utilizando parametros de ruta, si la respuesta es una lista vacia, significa que no existe una pelicula con el id suministrado",
)
def get_movies_by_id(id: int):
    return list(
        filter(lambda m: m["id"] == id, movie_list)
    )  # retorna "m" cuando el atributo "id" de m es identico al suministrado en la url

@app.get(
    "/movies/",
    tags=["Movies"],
    description="retorna una o mas  peliculas basandose en los atributos 'category' y 'year', los cuales son filtros.",
)
def get_movies_by_category_and_year(category: str):
    return list(filter(lambda m: category in m["category"], movie_list))

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
def post_movies(
    id: int = Body(),
    name: str = Body(),
    description: str = Body(),
    category: str = Body(),
    rating: float = Body(),
    cover_url: str = Body(),
):
    movie_list.append(
        {
            "id": id,
            "name": name,
            "description": description,
            "category": category,
            "rating": rating,
            "cover_url": cover_url,
        }
    )
#post Request para agregar pelicula a la lista

@app.put(
    "/movies/{id}",
    tags=["Movies"],
    description="actualiza una pelicula a la lista de movie_list"
)
def put_movies(
    id: int,
    name: str = Body(),
    description: str = Body(),
    category: str = Body(),
    rating: float = Body(),
    cover_url: str = Body(),
):
    
    for dic in movie_list:
     
        if dic['id'] == id:
            dic["name"]= name
            dic["description"]= description
            dic["category"]= category
            dic["rating"]= rating
            dic["cover_url"]= cover_url
            return {
                "message":"updated", 
                "dic":dic    
                    }
           

@app.delete(
    "/movies/{id}",
    tags=["Movies"],
    description="elimina una pelicula a la lista de movie_list"
)
def delete_movies(
    id: int,
):
    mindex = next((index for index ,movie in enumerate(movie_list) if movie['id'] == id))

    if mindex == None:
        return HTTPException(
            status_code=404,
            detail="no movie found, hence not deleting anything"
        )
    #delete movie
    dmovie = movie_list.pop(mindex)
    return {'message':'Movie deleted', 'dmovie':dmovie}




#endpoints relacionados con users creados apartir de aqui.
from pydantic import BaseModel, field_validator, validate_email
import re #regular expresions gods.
import ipdb

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

        


@app.get("/users", tags=['Users'])
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