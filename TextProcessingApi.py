from fastapi import FastAPI
from pydantic import BaseModel
from TextProcessing import preprocess

app_processing = FastAPI()

class SearchText(BaseModel):
    text: str

@app_processing.get("/")
async def root():
    return {"message": "Hello World"}

@app_processing.post("/")
async def search(searchText:SearchText):
    return {"processed_text": preprocess(searchText.text)}
