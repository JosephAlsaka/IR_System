from fastapi import FastAPI
from pydantic import BaseModel
from TextVectorization1 import vectorize1
from TextVectorization2 import vectorize2
app_vectorization = FastAPI()

class SearchText(BaseModel):
    text: str

@app_vectorization.get("/")
async def root():
    return {"message": "Hello World"}

@app_vectorization.post("/{id}/{option}")
async def search(searchText:SearchText,id:int,option:int):
    if(id==1):
        return {"vector":  vectorize1(searchText.text,option)}
    else:
        return {"vector":  vectorize2(searchText.text,option)}

    
