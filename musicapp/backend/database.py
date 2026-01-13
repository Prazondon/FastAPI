from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

sqlalchemy_database_url = "mysql+mysqlconnector://root:Coolvibes13*@db:3306/musicapp"

engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker (autocommit = False, autoflush= False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    