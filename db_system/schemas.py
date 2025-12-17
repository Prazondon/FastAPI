from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config: 
        orm_mode = True



class Token(BaseModel):
    access_token:str
    token_type:str
    

class AddTask(BaseModel):
    task_name: str
    task_deadline: str


class RemoveTask(BaseModel):
    task_name: str

    