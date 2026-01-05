from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_url = "mysql+mysqlconnector://root:Coolvibes13*@db:3306/taskmanager"

engine = create_engine(database_url, echo = True)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)


Base = declarative_base()

