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



class Students (BaseModel):
    name: str
    age: int 
    month: str


@app.post("/create-students/{student_id}")
def create_students(student_id: int, new_student: Students):
    if student_id in students:
        return {"Error": "Students Exists"}
    students[student_id] = new_student
    return students[student_id] 

