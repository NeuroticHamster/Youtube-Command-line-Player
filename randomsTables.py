#--- create database imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()


class Songinfo(Base):
    __tablename__ = 'songinfo'
    id = Column(Integer, primary_key=True)
    playlist = Column(String(50))
    artistname = Column(String(50))
    songname = Column(String(50))
    link = Column(String(100))

engine = create_engine('sqlite:///music.db')

Base.metadata.create_all(engine)
