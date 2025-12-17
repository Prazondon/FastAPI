from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User (Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)

    hashed_password =Column(String(255))
    
    boards = relationship ("Board", back_populates= "owner")

class Task(Base):

    __tablename__ = "boards"

    id = Column(Integer, primary_key= True, index= True)

    title = Column(String(100), unique=True, index=True)

    deadline = Column (String(100), index= True)

    owner_id = Column(Integer, ForeignKey("Users.id"))

    owner = relationship ("User", back_populates= "boards")



