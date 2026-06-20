from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model: str = "gemini-2.5-flash-lite", temperature: float = 0.3):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )