from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from musicapp.backend.database import get_db
from musicapp.backend.crud import get_top_artist, get_user_favourites
from musicapp.backend.redis_client import redis_client
import json

router = APIRouter()

@router.get("/top-artists")
def top_artists(db: Session = Depends(get_db)):
    cache_key = "top_artists"
    cached = redis_client.get(cache_key)
    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    artists = get_top_artist(db)
    artists_list = [artist.name for artist in artists]

    # Cache in Redis for 60s
    redis_client.setex(cache_key, 60, json.dumps(artists_list))

    return {"source": "db", "data": artists_list}


@router.get("/favorites/{user_id}")
def favorites(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"user:{user_id}:favorites"
    cached = redis_client.get(cache_key)
    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    favorites = get_user_favourites(db, user_id)
    favorites_list = [f.song_id for f in favorites]

    redis_client.setex(cache_key, 60, json.dumps(favorites_list))

    return {"source": "db", "data": favorites_list}
