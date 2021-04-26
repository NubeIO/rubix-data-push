import json

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://postgres:postgres@localhost:5432/thingsboard"


db = create_engine(db_string)
base = declarative_base()


class Film(base):
    __tablename__ = 'films'
    title = Column(String, primary_key=True)
    director = Column(String)
    year = Column(String)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)


# Read
songs_as_dict = []
films = session.query(Film)
for film in films:
    song_as_dict = {
        'year': film.year,
        'title': film.title,
        'director': film.director}
    songs_as_dict.append(song_as_dict)


j = json.dumps(songs_as_dict)
print(j)
