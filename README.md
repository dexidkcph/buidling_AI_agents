# Binance Docs AI Agent

This project builds an AI-powered agent that answers questions about Binance API documentation using retrieval and tool-based reasoning.

The system started as a Retrieval-Augmented Generation (RAG) foundation with chunking and search, and was then extended into a Day 4 agent using Pydantic AI.

## Overview

The goal of this project is to create a system that can:

- process Binance API documentation
- retrieve relevant information from the docs
- support grounded question answering
- power an AI agent with tool use

Instead of relying on a general-purpose language model alone, this system retrieves documentation first and answers based on that retrieved content.

## Pipeline

### 1. Load Documentation

- Source: Binance API documentation
- Markdown files are parsed into a structured format

### 2. Chunking

The documentation is split into meaningful chunks for retrieval.

Chunking approaches explored:

- section-based chunking (`my_chunks_sections`)
- sliding window chunking

Section-based chunking worked well because Binance documentation is highly structured and organized around endpoints, parameters, and explanations.

Example chunk:

```python
{
    "chunk": "...",
    "section": "...",
    "title": "...",
    "filename": "..."
};
```
### 3. Embeddings

The project uses SentenceTransformer to generate embeddings for semantic search.

- model: multi-qa-distilbert-cos-v1
- embeddings stored in: binance_embeddings

Each chunk is converted into a vector representation to enable similarity-based retrieval.

### 4. Search System

Three retrieval methods were implemented and compared.

#### Text Search

- keyword-based matching
- fast and interpretable
- strong for exact API terms such as recvWindow, timestamp, and endpoint names

#### Vector Search

- embedding-based retrieval
- handles paraphrased or natural language questions
- useful when query wording differs from the documentation

#### Hybrid Search

- combines text search and vector search
- removes duplicate results
- returns the top relevant chunks

Hybrid search was selected as the main retrieval strategy due to its balance of precision and recall.

---

## Agent Design

On Day 4, the retrieval system was extended into an AI agent using Pydantic AI.

A tool was created:

search_docs(query: str)

This tool:
- runs hybrid search on the documentation
- returns top relevant chunks
- formats results into readable text

### Agent Behavior

The agent is instructed to:

- always use the search tool before answering
- base answers only on retrieved documentation
- avoid hallucination or guessing
- clearly state when information is not found

This ensures responses are grounded in actual documentation.

---

## Example Usage

```python
result = await agent.run("How do I authenticate API requests?")
print(result.output)

```
## Key Findings

- Text search performs well on structured API documentation
- Vector search improves recall for natural language queries
- Hybrid search provides the most reliable results overall
- Tool-based agents are more accurate than standalone LLMs

## Challenges and Fixes

### Inconsistent function interfaces

Initial mismatch:

- text_search(query: str)
- vector_search(query, num_results=5)
- hybrid_search(query, num_results=5)

This caused runtime errors when combining results.

### Resolution

- adjusted hybrid_search to match actual function signatures
- removed unsupported parameters from text_search calls
- ensured consistent behavior across search layers

## Tech Stack

- Python
- Jupyter Notebook
- MinSearch
- Sentence Transformers
- NumPy
- Pydantic AI

## Project Structure

```text
aihero/
  ├── project/
  │   ├── binance.ipynb
  │   ├── index.ipynb
  │   ├── my_chunks_sections.json
  │   └── README.md
```
## What I Learned

- retrieval quality depends heavily on chunking
- structured docs benefit strongly from text search
- hybrid retrieval is more robust than a single method
- agents become useful when they can use tools
- debugging interfaces is critical in AI systems

## Limitations

- dependent on chunk quality
- no reranking implemented
- no evaluation metrics yet
- limited to single-step queries

## Next Steps

- add evaluation framework
- improve chunking strategy
- introduce reranking
- expand to multi-tool agents

## Course

https://alexeygrigorev.com/aihero/

## Author

Deheng Xie
