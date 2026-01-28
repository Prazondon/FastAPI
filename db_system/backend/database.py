from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_url = "postgresql://taskmanager_db_pf4f_user:m4Y0DH9bbrHMGnsTTLs7jw0CQzGCVKtH@dpg-d5sqbbk9c44c739fqkug-a/taskmanager_db_pf4f"

engine = create_engine(database_url, echo = True)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)


Base = declarative_base()

