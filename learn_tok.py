from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

# @app.get("/generate-token")
# def token():
#     return{
#         "token" : "1234"
#     }




# fake_token = "prajohn"

# @app.get("/protected_area")
# def authorize(authorization: str = Header(None)):
#     print("Swagger sent:", authorization)

#     if authorization != f"Bearer {fake_token}":
#         raise HTTPException(
#             status_code=401,
#             detail="You do not have the right token to access this"
#         )
#     return {"message": "You are welcomed"}



class Student (BaseModel):
    name: str
    age: int
    section : str


students_db = []

@app.post("/create-students")
def create_students(info: Student):
    students_db.append(info)
    return {"message": "Student saved", "data": info}

@app.get("/search-student")
def search_student(name: str):
    # Loop through the stored students
    for student in students_db:
        if student.name == name:
            return {
                "message": "Yes! the student exists",
                "data": student
            }
    
    return {"message": "The student does not exist"}



tok = "k1"

def dependen(authorization: str = Header(None)):
    # Check for "Bearer k1"
    if authorization != f"Bearer {tok}":
        raise HTTPException(
            status_code=401,
            detail="You do not have the right to access this"
        )
    return True

@app.get("/secret-document", dependencies=[Depends(dependen)])
def secret():
    return {"message": "You are learning quite good. KEEP IT UP"}


@app.get("/second-secret", dependencies=[Depends(dependen)])
def second_secret():
    return {"message": "Well DONE, Second time "}
