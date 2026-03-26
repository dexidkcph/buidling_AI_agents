# 🔧 AIHero – Binance Docs Chunking & Search (RAG Foundation)

## Overview

This project builds the foundation of a **Retrieval-Augmented Generation (RAG)** system using Binance API documentation.

The goal is to transform raw documentation into a system that can:
- retrieve relevant information  
- support AI agents  
- answer technical API questions  

---

## Data Pipeline

### Step 1 – Load Documentation
- Source: Binance API docs (GitHub)  
- Markdown files parsed into structured format  

---

### Step 2 – Chunking (Day 2)

The documentation is split into meaningful chunks using:

- section-based chunking (`my_chunks_sections`)  
- sliding window chunking (`my_chunks_simple`)  

Example chunk:

```python
{
  "chunk": "...",
  "section": "...",
  "title": "...",
  "filename": "..."
}

### Step 3 – Search System (Day 3)

Built three retrieval methods:

#### 1. Text Search (MinSearch)

```python
from minsearch import Index

text_index = Index(
    text_fields=["chunk", "title", "section", "filename"]
)
text_index.fit(binance_docs)
```

- keyword-based matching
- fast and interpretable

**Strong for:**
- exact API terms like `recvWindow`, `timestamp`, and endpoint names

---

#### 2. Vector Search (Embeddings)

```python
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")
```

- semantic similarity search
- handles paraphrased queries

**Strong for:**
- natural language questions

---

#### 3. Hybrid Search

```python
def hybrid_search(query, num_results=5):
    text_results = text_search(query, num_results=num_results)
    vector_results = vector_search(query, num_results=num_results)

    seen_ids = set()
    combined_results = []

    for result in text_results + vector_results:
        if result["id"] not in seen_ids:
            seen_ids.add(result["id"])
            combined_results.append(result)

    return combined_results[:num_results]
```

- combines both approaches
- removes duplicates

**Most robust overall**

---

## Example Queries

- How do I sign a Binance Spot API request?
- What does recvWindow mean?
- Why am I getting timestamp error?
- How do I place a market order?

---

## Key Findings

- Text search performs well due to structured API terminology
- Vector search improves recall for natural language queries
- Hybrid search gives the best balance

**Conclusion:**  
> Start simple with text search, then add hybrid if needed.

---

## What I Learned

- Retrieval quality depends more on structure than models
- Chunking strategy directly impacts performance
- Debugging data flow is harder than writing code

---

## Tech Stack

- Python
- MinSearch
- Sentence Transformers
- NumPy
- Jupyter Notebook

---

## Project Structure

```text
aihero/
  ├── project/
  │     ├── binance.ipynb
  │     ├── index.ipynb
  │     ├── my_chunks_sections.json
  │     └── README.md
```

---

## Next Step

- Connect retrieval to an LLM
- Build a full RAG pipeline
- Turn it into an AI agent
