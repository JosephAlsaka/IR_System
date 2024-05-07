from fastapi import FastAPI

from TextProcessing import preprocess

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/preprocess")
async def root():
    return {"message": preprocess("Hello World is the best")}