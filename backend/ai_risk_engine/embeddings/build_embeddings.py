import os
import numpy as np
import faiss
import pickle

from ai_risk_engine.embeddings.embedding_model import load_model
from ai_risk_engine.utils.text_cleaner import clean_text
from ai_risk_engine.utils.chunker import chunk_text

DATA_PATH = "./ai_risk_engine/confidential_data/"
VECTOR_PATH = "./ai_risk_engine/vector_store/"

model = load_model()

documents = []

metadata = []

for file in os.listdir(DATA_PATH):

    with open(DATA_PATH+"/"+file,'r',encoding="utf-8") as f:

        text = f.read()

        text = clean_text(text)

        chunks = chunk_text(text)

        for chunk in chunks:

            documents.append(chunk)

            metadata.append({
                "source":file,
                "text":chunk
            })

embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index,VECTOR_PATH+"faiss_index.bin")

with open(VECTOR_PATH+"metadata.pkl","wb") as f:

    pickle.dump(metadata,f)

print("Knowledge base built")