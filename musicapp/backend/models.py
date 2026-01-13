from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from musicapp.backend.database import Base

class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True, unique=True)

    name = Column(String(50), unique=True)
    songs_helper = relationship("Songs",back_populates="artist_helper")

class Songs (Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(200), unique=True)

    artist_id = Column(Integer, ForeignKey("artist.id"))

    artist_helper = relationship("Artist",back_populates="songs_helper")

class FavouriteSongs(Base):
    __tablename__ = "Fav_songs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    songs_id = Column(Integer, ForeignKey("songs.id"))