# Binance Docs AI Agent (Day 1–5)

This project builds an AI-powered agent that answers questions about Binance API documentation using retrieval, tool-based reasoning, and evaluation.

The system evolves across five stages:
- Day 1–2: Data processing and chunking
- Day 3: Search system (text, vector, hybrid)
- Day 4: Agent with tool usage
- Day 5: Evaluation and performance analysis

The goal is not just to build an agent, but to build a **measurable and improvable system**.

---

## Overview

This system:

- processes Binance API documentation
- retrieves relevant information using hybrid search
- answers questions grounded in documentation
- logs interactions for evaluation
- evaluates performance using structured metrics

Instead of relying on a general-purpose LLM, the system enforces:
> retrieve first → then answer

---

## Pipeline

### 1. Load Documentation (Day 1)

- Source: Binance API documentation
- Markdown files parsed into structured format

---

### 2. Chunking (Day 2)

Documentation is split into meaningful chunks for retrieval.

Approaches explored:

- section-based chunking (`my_chunks_sections`)
- sliding window chunking

Section-based chunking performed best due to structured API docs.

Example:

```python
{
    "chunk": "...",
    "section": "...",
    "title": "...",
    "filename": "..."
}
```

---

### 3. Embeddings (Day 3)

Semantic representations are created using SentenceTransformers.

- model: `multi-qa-distilbert-cos-v1`
- stored in: `binance_embeddings`

Each chunk is converted into a vector to enable similarity search.

---

### 4. Search System (Day 3)

Three retrieval methods were implemented:

#### Text Search
- keyword-based
- fast and interpretable
- strong for exact API terms

#### Vector Search
- embedding-based
- handles paraphrasing
- improves recall

#### Hybrid Search
- combines both approaches
- removes duplicates
- returns most relevant chunks

**Final decision:** Hybrid search → best balance of precision + recall

---

## Agent Design (Day 4)

The retrieval system is wrapped into an AI agent using Pydantic AI.

### Tool

```python
search_docs(query: str)
```

This tool:
- runs hybrid search
- returns top relevant chunks
- formats results for the agent

---

### Agent Behavior

The agent is instructed to:

- always call search before answering
- avoid hallucination
- answer only from retrieved content
- clearly say when information is missing

This creates a **grounded AI system**, not a guessing machine.

---

### Example Usage

```python
result = await agent.run("How do I authenticate API requests?")
print(result.output)
```

---

## Evaluation System (Day 5)

This is where the project becomes **serious**.

### 1. Logging System

Each interaction is stored as JSON:

```json
{
  "agent_name": "binance-agent",
  "agent_version": "v1",
  "source": "user",
  "messages": [...]
}
```

This enables reproducibility and analysis.

---

### 2. Evaluation Metrics

Each response is evaluated using an evaluation agent:

- instructions_follow
- answer_relevant
- answer_clear
- answer_citations
- completeness
- tool_call_search

---

### 3. AI-Generated Questions

Two types of test data:

- real user questions
- AI-generated questions

AI-generated questions:
- increase coverage
- expose edge cases
- stress-test the system

---

### 4. Data Analysis

Example workflow:

```python
import pandas as pd

df = pd.read_csv("evaluation_results.csv")

# Split by source
df_user = df[df["source"] == "user"]
df_ai = df[df["source"] == "ai-generated"]

# Split by version
df_v1 = df[df["agent_version"] == "v1"]
df_v2 = df[df["agent_version"] == "v2"]

print("V1:\n", df_v1.mean(numeric_only=True))
print("\nV2:\n", df_v2.mean(numeric_only=True))
print("\nUser Questions:\n", df_user.mean(numeric_only=True))
print("\nAI-generated Questions:\n", df_ai.mean(numeric_only=True))
```

---

## Key Findings

- Hybrid search significantly improves relevance
- Text search works well for structured API docs
- Vector search improves flexibility
- Agent performs better on real user queries
- AI-generated questions expose weaknesses

Weakest areas:
- citations
- completeness

---

## Challenges and Fixes

### Issue 1: Missing AI-generated results
- Cause: incorrect logging (`source` not set)
- Fix: added `source="ai-generated"`

### Issue 2: Mixed evaluation data
- Cause: v1 and v2 results combined
- Fix: split by `agent_version`

### Issue 3: Evaluation failures
- Cause: API limits / async issues
- Fix: batching and retry logic

### Issue 4: Search pipeline bugs
- Cause: incorrect field usage (`section` vs `content`)
- Fix: corrected extraction logic

---

## Tech Stack

- Python
- Jupyter Notebook
- Sentence Transformers
- NumPy
- Pydantic AI
- JSON / Pandas

---

## Project Structure

```text
aihero/
  ├── project/
  │   ├── index.ipynb
  |   ├── logging_utils.py
  |   ├── evaluation_results.csv
  │   ├── evals.py
  │   ├── run_evals.py
  │   ├── my_chunks_sections.json
  │   ├── logging_utils.py
  │   └── README.md
```

---

## What I Learned

- Chunking quality determines retrieval quality
- Hybrid search is more robust than single methods
- Agents need tools to be reliable
- Logging is critical for debugging AI systems
- Evaluation separates real systems from demos

---

## Limitations

- no reranking layer
- limited evaluation dataset
- single-step reasoning only
- citation quality is inconsistent

---

## Next Steps

- improve citation grounding
- add reranking layer
- evaluate on identical question sets across versions
- build API or UI interface
- extend to multi-agent system

---

## Course

https://alexeygrigorev.com/aihero/

---

## Author

Deheng Xie
