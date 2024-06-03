from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from TextProcessingApi import app_processing
from TextVectorizationApi import app_vectorization
from RankingApi import app_ranking
from pydantic import BaseModel
import httpx
app_main = FastAPI()

class SearchText(BaseModel):
    text: str
    
@app_main.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

#1 for antique
#2 for lotte
#1 with embedding
#2 without embedding
@app_main.post("/{id}/{option}")
async def search(searchText: SearchText, id: int,option:int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8001", json={"text": searchText.text})
        response_data = response.json()
        
    procced_text= response_data["processed_text"]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8002/{id}/{option}", json={"text": procced_text})
        response_data = response.json()
            
    vector=response_data["vector"]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8003/{id}/{option}", json=vector)
        response_data = response.json()
    return response_data
   
