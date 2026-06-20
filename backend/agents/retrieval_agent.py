from vector.store import add_documents, search
import uuid

SOURCE_COUNT_THRESHOLD = 8
TEXT_LENGTH_THRESHOLD = 6000

def retrieval_agent(state: dict) -> dict:
    sources = state.get("sources", [])
    raw_text = state.get("raw_text", "")

    use_vector_store = (
        len(sources) > SOURCE_COUNT_THRESHOLD
        and len(raw_text) > TEXT_LENGTH_THRESHOLD
    )

    if not use_vector_store:
        state["used_vector_store"] = False
        return state

    # Chunk raw_text back into pseudo-documents for embedding
    chunks = raw_text.split("\n\n")
    docs = [
        {"id": str(uuid.uuid4()), "text": chunk, "source": ""}
        for chunk in chunks if chunk.strip()
    ]

    add_documents(docs)
    relevant_chunks = search(state["query"], n_results=8)

    if relevant_chunks:
        state["raw_text"] = "\n\n".join(relevant_chunks)
        state["used_vector_store"] = True
    else:
        state["used_vector_store"] = False

    return state