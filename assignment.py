from fastapi import FastAPI, Header, HTTPException, Depends, Path
from pydantic import BaseModel


app = FastAPI()

class student (BaseModel):
    name: str
    age: int
    rank: int

token_number ="k123"
studentdb = []

def checker (authorization: str = Header(None)):
    if authorization!= f"Bearer {token_number}":
        raise HTTPException (
            status_code=401,
            detail= "You do not have the access to this endpoint"
        )
    return True



@app.get("/get-student", dependencies=[Depends(checker)])
def get_student ():
    return studentdb

@app.post("/create-student",dependencies=[Depends(checker)])
def create_student(Student_info: student):
    studentdb.append(Student_info)
    return studentdb


@app.get("/search-rank/{rank}", dependencies = [Depends(checker)])
def search_rank (rank: int = Path (...,description="Rank will come from the path")):
    for i in studentdb:
        if i.rank == rank:
            return i.name
    return {"message":"The student does not exist"}


## Response Model 


class StudentNameOnly (BaseModel):
    name: str 

@app.get("/get-names", response_model=list[StudentNameOnly])
def get_names ():
    return studentdb
