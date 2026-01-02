from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import model, schemas, crud, auth
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware




Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
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
def login(creds: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, creds.username)
    if not user or not crud.verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



Oauth2Scheme = OAuth2PasswordBearer(tokenUrl= "/auth/login")
def get_current_user (token:str = Depends(Oauth2Scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=401,
        detail=("Could not validate Credentials"),
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        user = crud.get_user_by_username(db, username)
        if user is None:
            raise credential_exception
        return user
    except JWTError:
        raise credential_exception
    except Exception as e:
        print(f"Error in get_current_user: {str(e)}")
        raise credential_exception
    





@app.post("/tasks", response_model=schemas.TaskRead)
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

@app.get("/tasks", response_model=list[schemas.TaskRead])
def get_tasks(current_user: model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(model.Task).filter(model.Task.owner_id == current_user.id).all()
    return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(model.Task).filter(
        model.Task.id == task_id,
        model.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or not owned by user"
        )

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


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

    
    



  