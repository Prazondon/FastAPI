from fastapi import FastAPI, Path

app1 = FastAPI()

students = {
    1: {
        "name": "Prajohn Hona",
        "age": 21,
        "height": "5 feet 7 inches"
    }
}



@app1.get("/")

def index():
    return {"name": "Prajohn Hona"}


@app1.get("/get_students/{student_id}")
def get_students(student_id: int = Path(..., description= "Enter the student id", gt = 0)):
    return students[student_id]


