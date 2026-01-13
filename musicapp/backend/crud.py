from sqlalchemy.orm import Session
from musicapp.backend.models import Songs, Artist, FavouriteSongs

def get_top_artist(db:Session, limit:int = 5 ):
    return db.query(Artist).join(Songs).group_by(Artist.id).order_by(function.count(Songs.id).desc()).limit(limit).all()

def get_user_favourites(db:Session, user_id: int):
    return db.query(FavouriteSongs).filter(FavouriteSongs.user_id == user_id).all()


