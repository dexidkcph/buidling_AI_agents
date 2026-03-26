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
}

