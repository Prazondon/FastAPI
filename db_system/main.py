from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import model, schemas, crud, auth
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from fastapi.middleware.cors import CORSMiddleware




Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud.create_user(db, user_in)
    return user

@app.post("/auth/login", response_model=schemas.Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not crud.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


Oauth2Scheme = OAuth2PasswordBearer(tokenUrl= "/auth/login")
def get_current_user (token:str = Depends(Oauth2Scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail=("Could not validate Credentials"),
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user = payload.get("sub")
        if user is None:
            raise credential_exception
        return user
    except:
        raise credential_exception
    





@app.post("/add-task")
def add_task(task: schemas.AddTask,  current_user: model.User = Depends(get_current_user), db: Session =Depends(get_db)):
    new_task = model.Task(
        title = task.title,
        deadline= task.deadline,
        owner_id = current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.post("/remove-task")
def remove_task(rem_task: schemas.RemoveTask, curren_user: model.User = Depends (get_current_user), db:Session = Depends(get_db)):
    task = db.query(model.Task).filter(
        model.Task.title == rem_task.title,
        
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or not owned by user"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

    
    



  