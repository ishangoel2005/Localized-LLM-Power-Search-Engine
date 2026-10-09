# Localized LLM Power Search Engine

> A Privacy Focused, Offline Capable **Multi-PDF Question Answering system** powered by **Retrieval-Augmented Generation (RAG)**, Semantic Search, Embeddings, Vector Databases and Local Large Language Models.

## Overview

**Localized LLM Power Search Engine** is an AI Powered document search and question-answering system designed to allow users to interact with multiple PDF documents using natural language.

Instead of manually searching through large documents, users can upload multiple PDFs and ask questions across them simultaneously. The system retrieves the most relevant document chunks using semantic similarity and provides context-grounded answers using a **locally hosted LLM**.

The project focuses on improving information retrieval while keeping the data and LLM inference **local**, making it suitable for privacy-sensitive use cases.

## Key Features

* **Multi-PDF Question Answering** - Query multiple documents simultaneously.
* **Semantic Search** - Retrieves relevant information based on meaning rather than exact keyword matches.
* **Retrieval-Augmented Generation (RAG)** - Grounds LLM responses using retrieved document context.
* **Embedding-Based Retrieval** - Converts document chunks and queries into vector representations.
* **Multi-Query Retrieval** - Generates multiple search perspectives for a single user query to improve retrieval.
* **Local LLM Support** - Uses locally hosted models through Ollama for privacy and offline inference.
* **Retrieval Evaluation** - Measures context precision and context utilization across benchmark questions.
* **Streamlit Interface** - Provides an interactive interface for document upload and question answering.

## Architecture

```text
                    ┌─────────────────────┐
                    │     PDF Documents   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Extraction   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Text Chunking      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Embedding Model     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
       Single-Query Search              Multi-Query Search
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Context    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Local LLM (Ollama)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Grounded Response   │
                    └─────────────────────┘
```

## How It Works

### 1. Document Ingestion

Users upload one or more PDF documents through the Streamlit interface.

The documents are processed and divided into smaller chunks so that relevant sections can be efficiently retrieved later.

### 2. Embedding Generation

Each document chunk is converted into a numerical vector using an embedding model.

These embeddings capture the semantic meaning of the text and allow the system to identify conceptually similar content.

### 3. Vector Retrieval

The generated embeddings are stored in a vector database.

When a user asks a question, the query is embedded and compared against the stored document vectors to retrieve the most relevant chunks.

### 4. Multi-Query Retrieval

For complex questions, the system can generate multiple variations of the original query.

Each variation is independently searched against the vector database, allowing the system to retrieve relevant information that may not be found using the original query alone.

### 5. Context-Grounded Generation

The retrieved document chunks are provided as context to the local LLM.

The model then generates an answer based on the retrieved information rather than relying entirely on its pretrained knowledge.

## Local AI Stack

The project supports local inference using **Ollama**, allowing both embedding generation and LLM inference to run locally.

### Models used in evaluation

* **Embedding:** `nomic-embed-text`
* **LLM:** `llama3.2`
* **Inference:** Local Ollama deployment

This approach reduces dependence on external APIs and helps keep uploaded documents within the local environment.

## Evaluation

A major focus of this project was **measuring retrieval quality rather than only demonstrating that the application works**.

A benchmark consisting of **30 questions** was used to compare different retrieval strategies.

### Evaluation Metrics

| Metric              | Purpose                                                                            |
| ------------------- | ---------------------------------------------------------------------------------- |
| Context Precision   | Measures how much of the retrieved context is relevant to the question             |
| Context Utilization | Measures how effectively the retrieved context contributes to the generated answer |
| Response Time       | Measures the computational overhead of retrieval and generation                    |

### Results

The multi-document RAG system achieved:

* **71% Context Precision**
* **99% Context Utilization**

The project also evaluated **Single-Query Retrieval vs Multi-Query Retrieval** to understand the trade-off between retrieval quality and computational cost.

> **Key observation:** Multi-query retrieval can provide additional retrieval perspectives, but generating and processing multiple queries introduces significant latency. This highlights the importance of balancing retrieval quality against inference cost.

## Tech Stack

### AI / ML

* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Embedding Models
* Semantic Search
* Multi-Query Retrieval

### Frameworks & Tools

* Python
* Streamlit
* Ollama
* Vector Database

### Models

* `nomic-embed-text`
* `llama3.2`

## Getting Started

### Prerequisites

Make sure you have:

* Python 3.x
* Ollama
* Git

Install Ollama and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Clone the Repository

```bash
git clone https://github.com/ishangoel2005/LOCALIZED-LLM-POWER-SEARCH-ENGINE.git
cd LOCALIZED-LLM-POWER-SEARCH-ENGINE
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

Open the Streamlit URL shown in your terminal and upload your PDF documents.

## Example Use Cases

The system can be used for:

* Research paper analysis
* Academic document search
* Technical documentation
* Internal organizational documents
* Reports and manuals
* Research and literature exploration
* Offline/private document analysis

## Future Improvements

Potential improvements include:

* Hybrid keyword + semantic retrieval
* Cross-encoder reranking
* Adaptive query expansion
* Better chunking strategies
* Citation-aware responses
* Retrieval caching
* Quantized local LLMs for lower resource usage
* Larger and more diverse evaluation datasets
* Automated hallucination and faithfulness evaluation
* Improved latency for multi-query retrieval
