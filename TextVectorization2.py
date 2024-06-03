import numpy as np
import joblib
from gensim.models import Word2Vec

model = Word2Vec.load("word2vectrainAntique3.model")
word_vectors=model.wv
vectorizer=joblib.load("vectorizer2.joblib")

def vectorize2(query,option):
    query_tfidf = vectorizer.transform([query])
    if option==1:
        query_embedding = embed_text_with_tfidf(query, query_tfidf, word_vectors, vectorizer)
        return query_embedding
    else:
        return query_tfidf.toarray().tolist()[0]


def get_word_embedding(word):
    try:
        return word_vectors[word]
    except KeyError:
        return None


def embed_text_with_tfidf(text, tfidf_vector, word_vectors, vectorizer):
    words = text.split()
    embeddings = []
    
    for word in words:
        word_embedding = get_word_embedding(word)
        if word_embedding is not None:
            word_index = vectorizer.vocabulary_.get(word)
            if word_index is not None:
                tfidf_value = tfidf_vector[0, word_index]
                embeddings.append(tfidf_value * word_embedding)
    
    if embeddings:
        return np.mean(embeddings, axis=0).tolist()
    else:
        return np.zeros(word_vectors.vector_size).tolist()





