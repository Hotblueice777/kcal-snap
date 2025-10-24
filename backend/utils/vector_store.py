# backend/utils/vector_store.py
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
from utils.build_knowledge import csv_to_docs

def build_faiss_index():
    """Build local FAISS index from CSV data"""
    docs = csv_to_docs()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    faiss.write_index(index, "faiss_index.bin")

    with open("faiss_texts.txt", "w", encoding="utf-8") as f:
        for line in docs:
            f.write(line + "\n")

    print(f"✅ FAISS index built: {len(docs)} items saved.")
    return index, model, docs

if __name__ == "__main__":
    build_faiss_index()
