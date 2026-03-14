import faiss
import pickle
import numpy as np
import os

from ai_risk_engine.embeddings.embedding_model import load_model

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

VECTOR_PATH = os.path.join(BASE_DIR,"vector_store")

model = load_model()

index = faiss.read_index(os.path.join(VECTOR_PATH,"faiss_index.bin"))

with open(os.path.join(VECTOR_PATH,"metadata.pkl"),"rb") as f:
    metadata = pickle.load(f)


def check_semantic_risk(prompt):

    prompt_embedding = model.encode([prompt])

    D,I = index.search(prompt_embedding,3)

    results = []

    for i,idx in enumerate(I[0]):

        distance = D[0][i]

        similarity = 1/(1+distance)

        doc = metadata[idx]

        results.append({

            "similarity":float(similarity),

            "source":doc["source"],

            "matched_text":doc["text"][:150]

        })

    max_similarity = max(r["similarity"] for r in results)

    return max_similarity, results