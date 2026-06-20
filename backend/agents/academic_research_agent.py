import requests
import uuid
import os
import xml.etree.ElementTree as ET

SEMANTIC_SCHOLAR_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

def fetch_semantic_scholar(query: str, limit: int = 5) -> list[dict]:
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,abstract,url,year,authors"
        }
        headers = {"x-api-key": SEMANTIC_SCHOLAR_KEY} if SEMANTIC_SCHOLAR_KEY else {}
        res = requests.get(url, params=params, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        results = []
        for paper in data.get("data", []):
            if not paper.get("abstract"):
                continue
            authors = ", ".join([a["name"] for a in paper.get("authors", [])[:3]])
            results.append({
                "id": str(uuid.uuid4()),
                "text": f"{paper['title']} ({paper.get('year', 'n.d.')})\nAuthors: {authors}\n{paper['abstract']}",
                "source": paper.get("url", "")
            })
        return results
    except Exception as e:
        print(f"Semantic Scholar fetch failed: {e}")
        return []

def fetch_arxiv(query: str, limit: int = 5) -> list[dict]:
    try:
        url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit
        }
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            link = entry.find("atom:id", ns).text.strip()
            results.append({
                "id": str(uuid.uuid4()),
                "text": f"{title}\n{summary}",
                "source": link
            })
        return results
    except Exception as e:
        print(f"arXiv fetch failed: {e}")
        return []

def fetch_pubmed(query: str, limit: int = 5) -> list[dict]:
    try:
        # Step 1: search for matching PubMed IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": limit,
            "retmode": "json"
        }
        search_res = requests.get(search_url, params=search_params, timeout=15)
        search_res.raise_for_status()
        ids = search_res.json().get("esearchresult", {}).get("idlist", [])

        if not ids:
            return []

        # Step 2: fetch abstracts for those IDs
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "rettype": "abstract",
            "retmode": "xml"
        }
        fetch_res = requests.get(fetch_url, params=fetch_params, timeout=15)
        fetch_res.raise_for_status()
        root = ET.fromstring(fetch_res.content)

        results = []
        for article in root.findall(".//PubmedArticle"):
            title_el = article.find(".//ArticleTitle")
            abstract_el = article.find(".//AbstractText")
            pmid_el = article.find(".//PMID")

            if title_el is None or abstract_el is None:
                continue

            title = "".join(title_el.itertext()).strip()
            abstract = "".join(abstract_el.itertext()).strip()
            pmid = pmid_el.text if pmid_el is not None else ""

            results.append({
                "id": str(uuid.uuid4()),
                "text": f"{title}\n{abstract}",
                "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })
        return results
    except Exception as e:
        print(f"PubMed fetch failed: {e}")
        return []

def academic_research_agent(state: dict) -> dict:
    query = state["query"]

    semantic_results = fetch_semantic_scholar(query)
    arxiv_results = fetch_arxiv(query)
    pubmed_results = fetch_pubmed(query)

    all_results = semantic_results + pubmed_results + arxiv_results

    if not all_results:
        state["raw_text"] = f"No academic papers were found for '{query}'. Try broadening the query or switch off Academic mode."
        state["sources"] = []
        state["status"] = "researched"
        return state

    state["sources"] = [r["source"] for r in all_results]
    state["raw_text"] = "\n\n".join([r["text"] for r in all_results])
    state["status"] = "researched"
    return state