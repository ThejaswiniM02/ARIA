from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.pipeline import build_pipeline
from db.database import init_db, save_research, get_history, get_research_by_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://aria-tau-liart.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
pipeline = build_pipeline()

class QueryRequest(BaseModel):
    query: str
    mode: str = "web"

@app.post("/research")
async def run_research(req: QueryRequest):
    initial_state = {
        "query": req.query.strip(),
        "raw_text": "",
        "sources": [],
        "key_facts": "",
        "comparison": "",
        "report": "",
        "status": "starting",
        "mode": req.mode
    }
    result = pipeline.invoke(initial_state)

    research_id = save_research(
        query=req.query,
        report=result["report"],
        sources=result["sources"]
    )

    return {
        "id": research_id,
        "report": result["report"],
        "sources": result["sources"],
        "key_facts": result["key_facts"],
        "status": result["status"],
        "used_vector_store": result.get("used_vector_store", False)
    }

@app.get("/history")
async def history():
    return {"items": get_history()}

@app.get("/research/{research_id}")
async def get_one(research_id: str):
    result = get_research_by_id(research_id)
    if not result:
        return {"error": "not found"}
    return result

@app.get("/health")
def health():
    return {"status": "ok"}