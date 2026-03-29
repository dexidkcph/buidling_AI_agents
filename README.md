# Binance API AI Agent

An AI-powered agent that answers Binance API questions using retrieval, hybrid search, and tool-based reasoning.

This project demonstrates how to build a production-style AI agent that is grounded in documentation instead of guessing.

---

<<<<<<< HEAD
## Overview

Most AI assistants hallucinate when answering technical API questions.

This project solves that by combining:

- Document ingestion from Binance API docs
- Hybrid search (text + semantic)
- Tool-based agent reasoning
- Grounded responses with context

The agent always retrieves relevant documentation before answering.

---

## Demo
=======
## Live App

https://binance-docs-agent.streamlit.app/

---

## Overview
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

### Main Demo (Agent in Action)

https://www.loom.com/share/YOUR_VIDEO_LINK

**Demo Question:**

I get a "timestamp for this request was 1000ms ahead of the server’s time" error when placing a signed order on Binance API — what causes it and how do I fix it?

---

<<<<<<< HEAD
### CLI Demo
=======
## Architecture
User → Streamlit UI → Agent → search_docs() → Hybrid Search
→
Text Search Vector Search
→
Retrieved Chunks
→
LLM Response

User → Streamlit UI → Agent → search_docs() → Hybrid Search
→
Text Search Vector Search
→
Retrieved Chunks
→
LLM Response
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

![CLI Demo](images/cli.gif)

---

<<<<<<< HEAD
### Streamlit App Demo

![Streamlit Demo](images/streamlit.gif)

---

## Features

- Hybrid search (text + vector)
- SentenceTransformer embeddings
- Tool-based agent (Pydantic AI)
- Grounded answers (no hallucination)
- Streamlit UI for interaction
- Evaluation pipeline

---

## Project Architecture

binance_docs/        # raw documentation  
binance_embeddings/  # vector storage  
app/                 # Streamlit app  
agent/               # agent logic  
eval/                # evaluation scripts  

---

## Pipeline
=======
## Core Components
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

### 1. Data Ingestion
- Load Binance API documentation (Markdown)
- Parse into structured format

### 2. Chunking
- Section-based chunking
- Preserves context for retrieval

### 3. Embeddings
- Model: multi-qa-distilbert-cos-v1
- Converts text into vectors for semantic search

### 4. Hybrid Search
Combines:
- Keyword search → exact matches
- Vector search → semantic similarity

### 5. Agent
- Built with Pydantic AI
- Uses search_docs() tool
- Always retrieves before answering

---

<<<<<<< HEAD
## Installation
=======
## Project Structure
app/

├── ingest.py # load + embedding pipeline

├── search_tools.py # text, vector, hybrid search

├── search_agent.py # agent + prompt

├── logs.py # interaction logging

├── main.py # CLI interface

├── app.py # Streamlit UI
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

git clone https://github.com/dexidkcph/buidling_AI_agents.git  
cd buidling_AI_agents 

Install dependencies:
uv sync  

Set environment variables:
OPENAI_API_KEY=your_key  

---

<<<<<<< HEAD
## Usage
=======
## Run Locally
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

Run Streamlit App:
streamlit run app/app.py  

<<<<<<< HEAD
Example Query:
What is recvWindow in Binance API?

---

## Evaluation
=======
```bash
uv sync
```

### 2. Set environment variable

Create `.env` in project root:

```env
OPENAI_API_KEY=your_key_here
```

### 3. Run CLI version

```bash
uv run python app/main.py
```

### 4. Run Streamlit app

```bash
uv run streamlit run app/app.py
```

## Example Questions

- How do I authenticate private endpoints?
- What is recvWindow used for?
- How do I place a signed order?
- What does timestamp mean in Binance API?

---

## Challenges & Fixes
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd

We tested:
- Retrieval accuracy
- Answer correctness
- Grounding quality

Results:

Version | Accuracy | Hallucination  
v1     | Medium  | High  
v2     | High    | Low  

---

<<<<<<< HEAD
## Challenges & Fixes

- Hallucination → fixed with tool usage  
- Retrieval quality → improved with hybrid search  
- Environment → fixed with .env  
- Performance → Streamlit caching  

---

## Tech Stack

- Python
- Streamlit
- SentenceTransformers
- Pydantic AI
- OpenAI API
- uv

---

## What I Learned

- Retrieval > prompting
- Hybrid search improves quality
- Agents need tools
- Evaluation is critical

---

## Future Improvements

- Add real-time Binance API testing
- Add reranking
- Add memory
- Deploy as API

---

## Author

Deheng Xie

---

## License

MIT
=======
## Key Takeaways

- Retrieval is more reliable than prompting alone  
- Hybrid search improves answer quality  
- Agents need tools to be trustworthy  
- Deployment introduces real-world constraints  
- Clean structure enables scalability  
>>>>>>> a745cc64e53c3359e4e6ba8d588c42fa48ea25fd
