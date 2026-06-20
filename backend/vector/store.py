import chromadb
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = chromadb.Client()
collection = client.get_or_create_collection(name="research_docs")

def embed_text(text: str) -> list[float]:
    result = genai.embed_content(model="models/text-embedding-004", content=text)
    return result["embedding"]

def add_documents(docs: list[dict]):
    if not docs:
        return
    try:
        embeddings = [embed_text(d["text"][:2000]) for d in docs]
        collection.add(
            documents=[d["text"] for d in docs],
            ids=[d["id"] for d in docs],
            metadatas=[{"source": d.get("source", "")} for d in docs],
            embeddings=embeddings
        )
    except Exception as e:
        print(f"Vector store add failed, continuing without it: {e}")

def search(query: str, n_results: int = 6) -> list[str]:
    try:
        query_embedding = embed_text(query)
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        print(f"Vector store search failed: {e}")
        return []