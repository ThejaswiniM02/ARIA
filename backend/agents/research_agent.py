from ddgs import DDGS
from vector.store import add_documents
import uuid

def research_agent(state: dict) -> dict:
    query = state["query"]
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=8):
            results.append({
                "id": str(uuid.uuid4()),
                "text": f"{r['title']}\n{r['body']}",
                "source": r["href"]
            })

    add_documents(results)

    state["sources"] = [r["source"] for r in results]
    state["raw_text"] = "\n\n".join([r["text"] for r in results])
    state["status"] = "researched"
    return state