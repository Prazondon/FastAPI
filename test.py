from fastapi import FastAPI, Header, HTTPException, Depends, Path, Body
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()



class Student(BaseModel):
    name: str
    age: int
    grade: str
    email: str

    class Config:
        orm_mode = True

## Fake ORM 
## ORM is connected to database so when SQLAlchemy brings the database to object based format it comes as below

class ORMStudent:
     def __init__(self, id, name, age, grade, email):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email

students_db = [
    ORMStudent(id=1, name="John", age=20, grade="A", email = "JOhn20A@gmailcom"),
    ORMStudent(id=2, name="Mira", age=22, grade="B", email = "Mira22B@gmailcom")
]

students_user_db = []


@app.get("/ORM-student",response_model=List[Student])
def get_student_ORM ():
    return students_db


@app.get("/id-student/{student_id}")
def student_by_id (student_id:int = Path(...,description="the id comes from the path")):
    for i in students_db:
        if i.id == student_id:
            return i
    else:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

## GET using response model include

@app.get("/get-student", response_model=List[Student], response_model_include= {"name"})
def get_student():
    return students_db


@app.post("/create-student")
def create_student(info:Student):
    students_user_db.append(info)
    return (f"the student has been registered{students_user_db}")

##UPDATE 
class Update_student(BaseModel):
    name: Optional [str]=None
    age: Optional [int]= None
    grade: Optional [str]=None
    email: Optional [str]=None



@app.put("/update-student/{student_id}")
def update_student(student_id: int, Update_stud: Update_student):
    for i in students_db:
        if i.id ==student_id:
            if i.name != None:
                i.name = Update_stud.name
            if i.age!= None:
                i.age = Update_stud.age
            if i.grade != None:
                i.grade = Update_stud.grade
            return i
            
        else:
            return{"message":"the student does not exist"}

## Delete BY ID


@app.delete("/delete-student/{student_id}")
def del_student(student_id:int):
    for i in students_db:
        if i.id == student_id:
            students_db.remove(i)
            return students_db
    raise HTTPException(
            status_code=404,
            detail="Student not found to delete"
        )

## Query Parameter

@app.get("/get-by-name/{name}")
def nameonly(name:str):
    for i in students_db:
        if i.name == name:
            return i
    raise HTTPException(
        status_code=404,
        detail="Not found"
    )


## API HEADER TEST

token = "goodtimes"

def checker_auth(authorization:str =Header(None)):
    if authorization == f"Bearer {token}":
        return True
    else:
        raise HTTPException(
            status_code=401,
            detail="Not allowed"
        )

@app.get("/get-student-info",dependencies=[Depends(checker_auth)])
def student_info():
    return students_db