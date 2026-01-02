from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    class Config: 
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str
    
class AddTask(BaseModel):
    title: str
    deadline: str = ""

class TaskRead(BaseModel):
    id: int
    title: str
    deadline: str = ""

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: int
    title: str
    deadline: str
    owner_id: int

    class Config:
        from_attributes = True

class RemoveTask(BaseModel):
    task_name: str