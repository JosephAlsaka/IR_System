from fastapi import FastAPI
from pydantic import BaseModel

from TextProcessing import preprocess

app = FastAPI()

class SearchText(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/preprocess")
async def get_preprocess():
    return {"message": preprocess("Hello World is the best")}

@app.post("/preprocess")
async def post_preprocess(searchText:SearchText):
    return {"message": preprocess(searchText.text)}