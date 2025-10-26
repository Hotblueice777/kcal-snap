# backend/assistant_rag.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# init Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# load FAISS index and text
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")

with open("faiss_texts.txt", "r", encoding="utf-8") as f:
    texts = [line.strip() for line in f.readlines() if line.strip()]


def rag_answer(question: str):
    """Use general GPT response when knowledge base search fails or similarity is too low."""

    # The smaller the FAISS distance, the higher the similarity. 
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb), k=3)

    # set a threshold
    if len(D[0]) == 0 or D[0][0] > 0.6:
        print("⚠️ Low similarity, switching to GPT fallback")
        return fallback_answer(question)

    context = "\n".join([texts[i] for i in I[0]])

    # Construct prompt and generate answer
    prompt = f"""
You are a concise and friendly nutrition assistant.
Use the context below to answer the question **only if relevant**.
If context is not clearly related, reply with a short general answer.

Please answer in under 80 words.

Context:
{context}

Question: {question}
"""

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ RAG call failed:", e)
        return fallback_answer(question)


def fallback_answer(question: str):
    """Fallback to general GPT response when knowledge base retrieval fails or similarity is too low."""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI nutrition assistant." "Please answer in under 80 words, focusing on key points."},
                {"role": "user", "content": question}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ Fallback GPT failed:", e)
        return "Sorry, I couldn’t find an answer right now."
