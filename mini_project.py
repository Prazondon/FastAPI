from jose import jwt, JWTError
from fastapi import FastAPI, Header,Body, Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta



app = FastAPI()




pwd_content = CryptContext(schemes = ["argon2"], deprecated = "auto")


def pass_has(password:str) -> str:
    return pwd_content.hash(password)

def verify_pass(password:str, hashed_password:str) -> bool:
    return pwd_content.verify(password, hashed_password)


db = {
    "username": "prajohn",
    "password": pass_has("hona")
}




@app.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    

    stored_hash = db["password"]

    if not verify_pass(password,stored_hash):
        return {"error":"Invalid"}
    else:
        
        thistoken
        return {"msg": "login successful", "access_token": thistoken}




SECRET_KEY = "thisisasecret123"
ALGORITHM = "HS256"


def create_token (db: dict, expires_delta: timedelta | None = None):
    to_encode = db.copy()
    if expires_delta:
        expires = datetime.utcnow()+ expires_delta
    else:
        expires = datetime.utcnow()+timedelta(minutes=60)
    
    to_encode ["exp"] = expires

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

# calling the create-token function and storing it in a variable
thistoken = create_token ({"sub": "prajohn"}, expires_delta=timedelta(minutes=15))


##next step is to validate that token 




Oauth2scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token:str = Depends(Oauth2scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail=("Could not validate Credentials"),
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload =jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user = payload.get("sub")
        if user is None:
            raise credential_exception
        return user
    except:
        raise credential_exception


@app.get("/protected-route")
def protected(current_user:dict = Depends(get_current_user)):
    return current_user