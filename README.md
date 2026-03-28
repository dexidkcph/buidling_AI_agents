# Binance Docs AI Agent

An AI-powered assistant that answers questions about Binance API documentation using retrieval-augmented generation (RAG), hybrid search, and tool-based reasoning.

This project evolves from raw documentation → structured retrieval → intelligent agent → deployed web app.

---

## 🚀 Live App

👉 https://binance-docs-agent.streamlit.app/

---

## 🧠 Overview

This system allows users to ask questions about Binance API and get **grounded, accurate answers** based on official documentation.

Instead of relying on a general LLM, the system:
1. Retrieves relevant documentation
2. Uses it as context
3. Generates a precise answer via an AI agent

---

## 🏗️ Architecture
User → Streamlit UI → Agent → search_docs() → Hybrid Search
↙ ↘
Text Search Vector Search
↓
Retrieved Chunks
↓
LLM Response

User → Streamlit UI → Agent → search_docs() → Hybrid Search
↙ ↘
Text Search Vector Search
↓
Retrieved Chunks
↓
LLM Response


---

## ⚙️ Core Components

### 1. Data Ingestion
- Loads Binance API documentation (markdown)
- Splits into structured chunks (section-based)

### 2. Embeddings
- Uses SentenceTransformers
- Converts text into vector representations

### 3. Hybrid Search
Combines:
- **Text search** (exact match)
- **Vector search** (semantic similarity)

Returns the most relevant documentation chunks.

### 4. Agent (Pydantic AI)
- Uses `search_docs()` as a tool
- Enforced behavior:
  - always search before answering
  - no hallucination
  - grounded responses only

### 5. Streamlit App
- Chat interface
- Cached system initialization
- Deployed to cloud

---

## 📁 Project Structure
app/
├── ingest.py # load + embedding pipeline
├── search_tools.py # text, vector, hybrid search
├── search_agent.py # agent + prompt
├── logs.py # interaction logging
├── main.py # CLI interface
├── app.py # Streamlit UI


---

## ▶️ Run Locally

### 1. Install dependencies

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

## 🧪 Example Questions

- How do I authenticate private endpoints?
- What is recvWindow used for?
- How do I place a signed order?
- What does timestamp mean in Binance API?

---

## ⚠️ Challenges & Fixes

- **Path issues**  
  → Fixed using `Path(__file__)` instead of relative paths  

- **Environment variables not loading**  
  → Fixed with `.env` + `load_dotenv()`  

- **Dependency issues**  
  → Managed with `uv`  

- **Slow app reloads**  
  → Fixed with `@st.cache_resource`  

---

## 📌 Key Takeaways

- Retrieval is more reliable than prompting alone  
- Hybrid search improves answer quality  
- Agents need tools to be trustworthy  
- Deployment introduces real-world constraints  
- Clean structure enables scalability  