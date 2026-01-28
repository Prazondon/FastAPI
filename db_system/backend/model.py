from sqlalchemy import Column, String, Integer, ForeignKey
from db_system.backend.database import Base
from sqlalchemy.orm import relationship

class User (Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True)
    

    hashed_password =Column(String(255))
    
    boards = relationship ("Task", back_populates= "owner")

class Task(Base):

    __tablename__ = "boards"

    id = Column(Integer, primary_key= True, index= True)

    title = Column(String(100), index=True)

    deadline = Column (String(100), index= True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship ("User", back_populates= "boards")



