from fastapi import FastAPI

app = FastAPI ()






@app.get("/create_api")

def index ():
    return {"name": "First Data"}




