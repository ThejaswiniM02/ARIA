# ARIA: Autonomous Research Intelligence Agent

A multi-agent AI research assistant that takes a query, sends it through four specialized agents, and returns a structured research report with sources.

**Live demo:** https://aria-tau-liart.vercel.app/

---

## What it does

You ask something like *"Compare UK scholarships for Indian students"* or *"Effects of sleep deprivation on memory"* — ARIA runs it through a pipeline of agents that each handle one part of the research process, then hands you back a full markdown report with citations.

Two modes:
- **Web mode** — searches the general web (DuckDuckGo) for broad, current information
- **Academic mode** — pulls from Semantic Scholar, arXiv, and PubMed for actual research-paper-backed answers

---

## How it works
User Query

↓

Research Agent     →  Collects sources (web + academic)

↓

Analysis Agent     →  Extracts key facts and arguments

↓

Comparison Agent   →  Identifies patterns, contrasts, consensus

↓

Writer Agent       →  Produces structured report with citations

Built with **LangGraph** for orchestration — each agent is a node, edges define what runs next, with conditional branching for web vs academic mode.

---

## Stack

**Backend**
- FastAPI
- LangGraph (agent orchestration)
- Gemini API (`gemini-2.5-flash-lite`) for all LLM calls
- ChromaDB (conditional vector retrieval for large result sets)
- SQLite (research history)

**Frontend**
- Next.js 14 + TypeScript
- Tailwind CSS
- React Markdown + remark-gfm (renders tables properly)

---

## Features

- 4-agent pipeline with a live visual progress tracker (watch each agent light up as it works)
- Web search + Academic search toggle
- Persistent research history — past reports saved and reloadable without re-running the pipeline
- Adaptive retrieval — automatically decides whether a query needs vector-based retrieval based on source count and text length, instead of always using it
- Graceful degradation — if any individual data source (Semantic Scholar, arXiv, PubMed, vector store) fails or rate-limits, the pipeline continues with whatever it has rather than crashing

---

## Running locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

You'll need a free Gemini API key in `backend/.env`:
GEMINI_API_KEY=your_key_here

---

## Why I built this

Most of my other projects (DiseaseDetector, VisionForAll) are single-model AI tools. ARIA was built to demonstrate **agentic AI** specifically — orchestrating multiple specialized agents that pass state between each other, rather than one model doing everything in a single prompt. This pattern (research → analyze → compare → write) is closer to how real agentic systems are being built in production right now.

---

## What's next

- Persistent Postgres (Supabase) instead of SQLite, so history survives redeploys
- Semantic Scholar API key (currently using public/unauthenticated endpoint, pending approval)
- Source-similarity search across past research using the vector store
