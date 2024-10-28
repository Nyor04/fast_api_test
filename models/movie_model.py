from sqlalchemy import Column, Integer, String, Float
from models_config.db_manager import Base 



class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    