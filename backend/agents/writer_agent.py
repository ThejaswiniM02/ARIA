from utils.gemini_client import get_llm
from langchain_core.messages import HumanMessage

def writer_agent(state: dict) -> dict:
    llm = get_llm()
    query = state["query"]
    facts = state["key_facts"]
    comparison = state["comparison"]
    sources = state.get("sources", [])

    sources_text = "\n".join(sources[:5])

    prompt = f"""
You are a professional report writer. Write a detailed research report on: "{query}"

Key Facts:
{facts}

Comparison / Breakdown:
{comparison}

Write in markdown. Include:
- Executive Summary
- Key Findings
- Detailed Comparison
- Conclusion
- Sources section at the end

Sources available:
{sources_text}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    state["report"] = response.content
    state["status"] = "done"
    return state