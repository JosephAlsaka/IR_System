from fastapi import FastAPI
from pydantic import BaseModel

from TextProcessing import preprocess

app = FastAPI()

class SearchText(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search/{id}")
async def search(searchText:SearchText,id:int):
    return {"results": [preprocess(searchText.text)]}