# backend/assistant_rag.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import AzureOpenAI
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# 初始化 Azure OpenAI 客户端
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

# 模型部署名（你在 Azure 上的 deployment name）
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# 加载 FAISS 索引和文本
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")

with open("faiss_texts.txt", "r", encoding="utf-8") as f:
    texts = [line.strip() for line in f.readlines() if line.strip()]


def rag_answer(question: str):
    """主函数：先查本地知识库，如匹配度低则fallback到GPT通用回答"""

    # === 1️⃣ 检索最相似段落 ===
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb), k=3)

    # FAISS返回的距离越小越相似，这里设阈值（>0.8表示相似度太低）
    if len(D[0]) == 0 or D[0][0] > 0.8:
        print("⚠️ Low similarity, switching to GPT fallback")
        return fallback_answer(question)

    context = "\n".join([texts[i] for i in I[0]])

    # === 2️⃣ 构造提示并生成回答 ===
    prompt = f"""
You are a helpful nutrition assistant. 
Use the context below to answer the question as accurately as possible.

Context:
{context}

Question: {question}
"""

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ RAG call failed:", e)
        return fallback_answer(question)


def fallback_answer(question: str):
    """若知识库检索失败或匹配度太低，改为通用GPT回答"""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI nutrition assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ Fallback GPT failed:", e)
        return "Sorry, I couldn’t find an answer right now."
