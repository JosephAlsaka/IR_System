from fastapi import FastAPI
from pydantic import BaseModel
from Ranking1 import search1
from Ranking2 import search2    
app_ranking = FastAPI()


@app_ranking.get("/")
async def root():
    return {"message": "Hello World"}

@app_ranking.post("/{id}/{option}")
async def search(vec :list[float],option:int,id:int):
    if(id==1):
        return {"result":  search1(vec,option)}
    
    else:
        return {"result":  search2(vec,option)}

    
