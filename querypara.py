from fastapi import FastAPI
from typing import Optional

app = FastAPI()


students = {
    1: {
        "name" :"Prajohn Hona",
        "age" : 21
    }
}




@app.get('/get-by-name')
def get_students(name : Optional[str] = None):
    for students_id in students:
        if students[students_id]["name"] == name:
            return students[students_id]
    return ("Data not found ")