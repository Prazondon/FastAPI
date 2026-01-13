from fastapi import FastAPI
from musicapp.backend.routes import router
from musicapp.backend.database import Base, engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)
