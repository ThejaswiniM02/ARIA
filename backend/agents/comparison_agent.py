from utils.gemini_client import get_llm
from langchain_core.messages import HumanMessage

def comparison_agent(state: dict) -> dict:
    llm = get_llm()
    facts = state["key_facts"]
    query = state["query"]

    prompt = f"""
You are a comparison specialist. Based on these key facts about "{query}":

{facts}

Create a structured comparison table or breakdown. Use markdown formatting.
Group similar items. Highlight differences clearly.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    state["comparison"] = response.content
    state["status"] = "compared"
    return state