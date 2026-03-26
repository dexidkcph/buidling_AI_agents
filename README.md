AIHero – Binance Docs Chunking & Search (RAG Foundation)

Overview

This project builds the foundation of a Retrieval-Augmented Generation (RAG) system using Binance API documentation.

The goal is to transform raw documentation into a system that can:

retrieve relevant information
support AI agents
answer technical API questions

Data Pipeline
Step 1 – Load Documentation
Source: Binance API docs (GitHub)
Markdown files parsed into structured format
Step 2 – Chunking (Day 2)

The documentation is split into meaningful chunks using:

section-based chunking (my_chunks_sections)
sliding window chunking (my_chunks_simple)

Example chunk:

{
  "chunk": "...",
  "section": "...",
  "title": "...",
  "filename": "..."
}

Insight:

Section chunks = better context
Small chunks = higher recall but more noise
Step 3 – Search System (Day 3)

Built three retrieval methods:

1. Text Search (MinSearch)
text_index = Index(
    text_fields=["chunk", "title", "section", "filename"]
)
text_index.fit(binance_docs)
keyword-based matching
fast and interpretable

Strong for:
exact API terms (recvWindow, timestamp, endpoints)

2. Vector Search (Embeddings)
embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")
semantic similarity search
handles paraphrased queries

Strong for:
natural language questions
indirect phrasing

3. Hybrid Search
def hybrid_search(query):
    return text_results + vector_results
combines both approaches
removes duplicates

Most robust overall

Example Queries
How do I sign a Binance Spot API request?
What does recvWindow mean?
Why am I getting timestamp error?
How do I place a market order?

Key Findings
Text search performs surprisingly well due to structured API terminology
Vector search improves recall for natural language queries
Hybrid search gives the best balance

Conclusion:

Start simple (text search), add hybrid if needed

What I Learned
Retrieval quality depends more on chunking and structure than models
Fancy AI ≠ better results
Debugging data flow (not models) is the real challenge

Tech Stack
Python
MinSearch
Sentence Transformers
NumPy
Jupyter Notebook

Project Structure
aihero/
  ├── project/
  │     ├── day2_chunking.ipynb
  │     ├── day3_search.ipynb
  │     ├── my_chunks_sections.json
  │     └── README.md

Next Step
Connect retrieval to LLM
Build full RAG pipeline
Turn into AI agent for Binance API assistance
