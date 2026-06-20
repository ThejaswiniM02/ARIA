from utils.gemini_client import get_llm
from langchain_core.messages import HumanMessage

def analysis_agent(state: dict) -> dict:
    llm = get_llm()
    raw = state["raw_text"]
    query = state["query"]

    prompt = f"""
You are a research analyst. Given the following raw research text, extract the key facts relevant to: "{query}"

Raw text:
{raw[:4000]}

Return a bullet-point list of key facts only. Be concise.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    state["key_facts"] = response.content
    state["status"] = "analyzed"
    return state