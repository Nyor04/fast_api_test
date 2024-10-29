from fastapi import FastAPI

from routers.movies import movie_router
from routers.auth import auth_router
from routers.users import users_router

from models_config.db_manager import engine, Base, sqlite_file_name, base_dir

from os import path


app = FastAPI(
    title="The Anything API",
    version="1.0",
    description="Fast API Learning and testing - Hello World!",
)  

if path.exists(path.join(base_dir,sqlite_file_name)):
    pass #si la DB existe, pues no hagas mas nada mijo.
else:
    Base.metadata.create_all(bind=engine) #creacion de la DB descrita en models.movie_db

##importing routers:
app.include_router(movie_router)
app.include_router(auth_router)
app.include_router(users_router)