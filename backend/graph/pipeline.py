from langgraph.graph import StateGraph, END
from agents.research_agent import research_agent
from agents.academic_research_agent import academic_research_agent
from agents.retrieval_agent import retrieval_agent
from agents.analysis_agent import analysis_agent
from agents.comparison_agent import comparison_agent
from agents.writer_agent import writer_agent
from typing import TypedDict

class ResearchState(TypedDict):
    query: str
    raw_text: str
    sources: list
    key_facts: str
    comparison: str
    report: str
    status: str
    mode: str
    used_vector_store: bool

def route_research(state: ResearchState) -> str:
    return "academic" if state.get("mode") == "academic" else "web"

def build_pipeline():
    graph = StateGraph(ResearchState)

    graph.add_node("web_research", research_agent)
    graph.add_node("academic_research", academic_research_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("analysis", analysis_agent)
    graph.add_node("comparison", comparison_agent)
    graph.add_node("writer", writer_agent)

    graph.set_conditional_entry_point(
        route_research,
        {
            "web": "web_research",
            "academic": "academic_research",
        }
    )

    graph.add_edge("web_research", "retrieval")
    graph.add_edge("academic_research", "retrieval")
    graph.add_edge("retrieval", "analysis")
    graph.add_edge("analysis", "comparison")
    graph.add_edge("comparison", "writer")
    graph.add_edge("writer", END)

    return graph.compile()