from pinecone import Pinecone, ServerlessSpec
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


pc = Pinecone(api_key="fc6af30d-7243-4116-9d91-ab683be1d8ff")
index=pc.Index("antique")
tfidf_matrix=joblib.load("tfidf_matrix_antique.joblib")
corpusList=joblib.load("corpusListantique.joblib")

def withoutEmbedding(vec,k):
    results = cosine_similarity(tfidf_matrix,[vec])
    results = results.flatten() 
    top_k_indices = np.argsort(results)[-k:][::-1]
    top_k_ids = [corpusList[idx]['text'] for idx in top_k_indices]
    return top_k_ids

def search1(vec,option):
    if option==1:
        vectors=index.query(
            namespace="ns1",
            vector=vec,
            top_k=10,
            include_values=False,
            include_metadata=True
        )
        
        return  [text['metadata']['text'] for text in vectors['matches']]
    else:
        result=withoutEmbedding(vec,10)
        return result
        
