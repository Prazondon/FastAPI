from fastapi import FastAPI
from fastapi import Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


students = {
    1: {
        "name" :"Prajohn Hona",
        "age" : 21,
        "month": "October"
    }
}


@app.get("/")
def index ():
    return students


@app.get("/get_students/{student_id}")
def get_students(student_id: int = Path (..., description= "Enter the student id", gt = 0)):
    return students[student_id]




@app.get('/get-by-name')
def get_students(name : str):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return ("Data not found ")



class Students (BaseModel):
    name: str
    age: int 
    month: str

class UpdateStudent (BaseModel):
    name : Optional[str] =None
    age : Optional[int] =None
    year : Optional[str] =None

    

@app.post("/create-students/{student_id}")
def create_students(student_id: int, new_student: Students):
    if student_id in students:
        return {"Error": "Students Exists"}
    students[student_id]= new_student.dict()
    return students[student_id] 

@app.put("/update-students/{student_id}")
def update_student(student_id: int, up_students : UpdateStudent):
    if student_id not in students:
        return {"Error": "Student not found"}
    if up_students.name != None:
        students[student_id].name =up_students.name
    elif up_students.age != None:
        students[student_id].age =up_students.age
    elif up_students.year != None:
        students[student_id].year =up_students.year   
    return students[student_id]



@app.delete("/delete-student/ {student_id}")
def delete_student (student_id : int):
    if students[student_id] not in students:
        return {"The student does not exist"}
    del students[student_id]
    return {"The student has been deleted"}