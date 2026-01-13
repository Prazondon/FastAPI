from fastapi import FastAPI

app = FastAPI ()

@app.get("/")
def home():
    return "yes this is a test"
