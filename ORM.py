from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()



class Student(BaseModel):
    name: str
    age: int
    grade: str

    class Config:
        orm_mode = True

## Fake ORM 
## ORM is connected to database so when SQLAlchemy brings the database to object based format it comes as below

class ORMStudent:
     def __init__(self, id, name, age, grade):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade

students_db = [
    ORMStudent(id=1, name="John", age=20, grade="A"),
    ORMStudent(id=2, name="Mira", age=22, grade="B")
]



@app.get("/ORM-student",response_model=List[Student])
def get_student_ORM ():
    return students_db