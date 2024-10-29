

from sqlalchemy import select, update, delete, and_
from models.movie_model import Movie as MovieModel


class MovieService():
    def __init__(self, session):
        self.session = session

    def get_movies(self):
        query = self.session.query(MovieModel).all()
        movie_list = [movie.__dict__ for movie in query]
        return movie_list
    
    def get_movie(self, id):
        query = select(MovieModel).filter(MovieModel.id == id)
        result = self.session.execute(query).scalars().all()
        return result
    
    def get_movies_by_category_and_year(self,category:str, year:int):
        query = select(MovieModel).filter(and_(MovieModel.category == category, MovieModel.year == year))
        result = self.session.execute(query).scalars().all()
        return result
    
    def post_movie(self, **kwargs):
        new_movie = MovieModel(**kwargs.model_dump())
        self.session.add(new_movie)
        self.session.commit()
        return

    def put_movie(self, id, **kwargs):
        query = update(MovieModel).where(MovieModel.id == id).values(**kwargs.model_dump())
        self.session.execute(query)
        self.session.commit()
        return

    def delete_movie(self, id):
        query = delete(MovieModel).where(MovieModel.id == id)
        self.session.execute(query)
        self.session.commit()
        return