import json
import numpy as np
from pathlib import Path
from minsearch import Index
from sentence_transformers import SentenceTransformer


def load_chunks(json_path: str):
    """
    Load the pre-chunked Binance documentation from JSON.
    """
    path = Path(json_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_binance_docs(raw_chunks):
    """
    Normalize raw chunk data into a consistent structure.
    """
    binance_docs = []

    for i, doc in enumerate(raw_chunks):
        binance_docs.append({
            "id": i,
            "chunk": doc.get("content", ""),
            "title": doc.get("title", ""),
            "description": doc.get("description", ""),
            "filename": doc.get("filename", ""),
            "section": doc.get("section", "")
        })

    return binance_docs


def build_text_index(binance_docs):
    """
    Build exact-match text search index.
    """
    text_index = Index(
        text_fields=["chunk", "title", "description", "filename", "section"],
        keyword_fields=[]
    )
    text_index.fit(binance_docs)
    return text_index


def load_embedding_model(model_name: str = "multi-qa-distilbert-cos-v1"):
    """
    Load the sentence transformer used for semantic search.
    """
    return SentenceTransformer(model_name)


def build_vector_index(binance_docs, embedding_model):
    """
    Convert all chunks into embeddings for vector search.
    """
    texts = [doc["chunk"] for doc in binance_docs]
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings)
    return embeddings


def initialize_search_system(json_path: str):
    """
    Full setup:
    - load data
    - normalize docs
    - build text index
    - load embedding model
    - build vector embeddings
    """
    raw_chunks = load_chunks(json_path)
    binance_docs = build_binance_docs(raw_chunks)
    text_index = build_text_index(binance_docs)
    embedding_model = load_embedding_model()
    vector_embeddings = build_vector_index(binance_docs, embedding_model)

    return {
        "binance_docs": binance_docs,
        "text_index": text_index,
        "embedding_model": embedding_model,
        "vector_embeddings": vector_embeddings,
    }


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    json_path = project_root / "my_chunks_sections.json"

    data = initialize_search_system(str(json_path))
    print("Docs loaded:", len(data["binance_docs"]))