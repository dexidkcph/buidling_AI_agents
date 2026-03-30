# Binance API AI Agent

An AI-powered agent that answers Binance API questions using retrieval, hybrid search, and tool-based reasoning.

This project demonstrates how to build a production-style AI agent that is grounded in documentation instead of guessing.

---

## Overview

Most AI assistants hallucinate when answering technical API questions.

This project solves that by combining:

- Document ingestion from Binance API docs
- Hybrid search (text + semantic)
- Tool-based agent reasoning
- Grounded responses with context

The agent always retrieves relevant documentation before answering.

Live app at Streamlit: https://binance-docs-agent.streamlit.app/

---

## Demo

### Main Demo (Agent in Action)

This demo shows the agent diagnosing a real Binance API error using retrieval and tool-based reasoning.

<a href="https://www.loom.com/share/796f6995b3a64ec5b1ea8c9a1a0ca688">
  <img src="images/demo.png" width="700">
</a>

---

### Demo Questions

**1. Timestamp Error Debugging**

I get a "timestamp for this request was 1000ms ahead of the server’s time" error when placing a signed order on Binance API — what causes it and how do I fix it?

**2. Authentication & Signature**

How do I authenticate a signed request on Binance API, what parameters are required (API key, signature, timestamp, recvWindow), and can you show a complete example of generating the signature?

---

### CLI Demo

```bash
uv run main.py
```

This opens an interactive CLI environment. You can ask the conversational agent any question about Binance.

<p align="left">
  <img src="images/cli.gif" width="700">
</p>
Type `stop` to exit

---

### Streamlit App Demo

<p align="left">
  <img src="images/streamlit.gif" width="700">
</p>

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

## Installation


```bash
git clone 

```
https://github.com/dexidkcph/buidling_AI_agents.git  


```bash
cd buidling_AI_agents

```

Install dependencies:
```bash
uv sync
```

Set environment variables:
```bash
OPENAI_API_KEY=your_key 
```

---

## Usage

Run Streamlit App:
```bash
uv run streamlit run app/app.py
```

Example Query:
```bash
What is recvWindow in Binance API?
```


---

## Evaluations

Evaluation is a critical component of this project to ensure the agent produces grounded and reliable answers.

### Evaluation Criteria

We evaluate the agent across the following dimensions:

- `instructions_follow` – The agent follows the user's request
- `instructions_avoid` – The agent avoids restricted or irrelevant actions
- `answer_relevant` – The response directly answers the question
- `answer_clear` – The response is clear and understandable
- `answer_citations` – The answer is grounded in retrieved documentation
- `completeness` – The response covers all important aspects
- `tool_call_search` – The agent correctly uses the retrieval tool

---

### Evaluation Pipeline

The evaluation is performed in two stages:

1. **Synthetic Data Generation**
   - Questions are generated to simulate real user queries
   - Covers authentication, errors, parameters, and order placement
   - See: `eval/data-gen.ipynb`

2. **Agent Evaluation**
   - The agent answers each question
   - Responses are scored across all criteria
   - See: `eval/evaluations.ipynb`

---

### Results

| Metric               | Score (%) |
|---------------------|----------|
| instructions_follow | 100      |
| instructions_avoid  | 100      |
| answer_relevant     | 100      |
| answer_clear        | 100      |
| answer_citations    | 100      |
| completeness        | 70       |
| tool_call_search    | 100      |

---

## Project Structure

This project is organized into modular components covering data ingestion, retrieval, agent logic, UI, and evaluation.

### Core Application

- `app/app.py`  
  Streamlit-based web interface for interacting with the AI agent  
  - Chat-style UI  
  - Displays responses from the agent  
  - Uses caching for performance  

---

### Data Pipeline

- `ingest.py`
  Handles loading and preprocessing of Binance API documentation  
  - Parses Markdown files  
  - Splits into structured sections  
  - Prepares data for embedding  

- `chunking logic` 
  - Section-based chunking  
  - Preserves context for better retrieval  

---

### Retrieval System

- `search.py` / `hybrid_search()`  
  Implements hybrid retrieval:
  - Text search (keyword matching)  
  - Vector search (semantic similarity using embeddings)  
  - Combines and ranks results  

- `binance_embeddings/`  
  Stores vector embeddings for semantic search  

---

### Agent

- `agent.py` *(or equivalent)*  
  Defines the AI agent using Pydantic AI  
  - Uses `search_docs(query)` as a tool  
  - Enforces retrieval before answering  
  - Prevents hallucination  

---

### Evaluation

- `eval/data-gen.ipynb`  
  Generates synthetic evaluation questions  

- `eval/evaluations.ipynb`  
  Runs evaluation pipeline and computes metrics  

---

### Logs / Debugging *(if applicable)*

- Logs responses and agent behavior for debugging and analysis  

---

## Deployment

### Local Run

```bash
uv run streamlit run app/app.py
```

### Streamlit Cloud Deployment

1. Export dependencies:

```bash
uv export > requirements.txt
```

2. Push to GitHub

3. Go to Streamlit Cloud and deploy your repo

4. Set environment variable:

```
OPENAI_API_KEY=your_key
```

5. App will auto-deploy on every push

---


### Key Insights

- The agent performs strongly on **relevance and correctness** (`100%`)
- Retrieval grounding is effective (`answer_citations = 100%`)
- Tool usage is reliable (`tool_call_search = 100%`)

However:

- `completeness` is lower (70%), indicating that:
  - Some answers miss edge cases or deeper explanations
  - The agent may retrieve correct context but not fully synthesize it

---

### Improvements

- Increase evaluation dataset size (currently limited to ~10 questions)
- Add more complex, multi-step queries (e.g. debugging API errors)
- Introduce adversarial questions to test robustness
- Improve answer synthesis to increase completeness

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

## Credits / Acknowledgments

- [DataTalksClub](https://github.com/DataTalksClub) for open-source course materials  
- [Alexey Grigorev](https://www.linkedin.com/in/agrigorev) for the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/)  
- SentenceTransformers for embeddings  
- Streamlit for UI  
- Pydantic AI for agent framework

## License

MIT
