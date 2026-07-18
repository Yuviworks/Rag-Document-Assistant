# Technical Documentation Assistant

A Retrieval-Augmented Generation (RAG) application that answers technical questions using a custom documentation corpus. The application retrieves relevant information from indexed documents and generates grounded responses using a Large Language Model.

---

# Author

**Yuvraj Vethekar**

Computer Engineering Student | AI & Data Science Enthusiast

GitHub: https://github.com/Yuviworks
---

# Features

- 📄 Document ingestion from `.txt` and `.md` files
- ✂️ Automatic document chunking
- 🧠 Semantic embeddings using Sentence Transformers
- 💾 ChromaDB vector database
- 🔍 Query rewriting for improved retrieval
- ✅ LLM-based document relevance grading
- 🔄 Retry mechanism with query reformulation
- 🤖 Answer generation using Groq Llama 3.3 70B
- 📚 Source citation
- 🌐 FastAPI backend
- 🖥️ Streamlit frontend

---

# Technology Stack

- Python
- FastAPI
- Streamlit
- LangChain
- LangGraph
- ChromaDB
- Sentence Transformers
- Groq API
- Pydantic

---

# Project Structure

```
Technical-Documentation-Assistant/

│── app.py
│── main.py
│── ingest.py
│── rag_workflow.py
│── requirements.txt
│── README.md
│
├── documents/
│   ├── langchain_docs.txt
│   ├── langgraph_docs.txt
│   ├── fastapi_docs.txt
│   ├── chromadb_docs.txt
│   └── pydantic_docs.txt
│
└── chroma_db/
```

---

# Architecture

```
User
   │
   ▼
Streamlit UI
   │
   ▼
FastAPI Backend
   │
   ▼
LangGraph Workflow
   │
   ├── Query Analysis
   ├── Document Retrieval
   ├── Document Grading
   ├── Retry (if needed)
   └── Answer Generation
   │
   ▼
Response with Source Documents
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/Yuviworks/Technical-Documentation-Assistant.git

cd Technical-Documentation-Assistant
```

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python -m venv venv

source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Application

## Step 1: Ingest Documents

```bash
python ingest.py
```

## Step 2: Start FastAPI

```bash
uvicorn main:app --reload
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

## Step 3: Run Streamlit

```bash
streamlit run app.py
```

---

# API Endpoints

## POST /query

Request

```json
{
  "question": "What is LangGraph?"
}
```

Response

```json
{
  "question": "What is LangGraph?",
  "answer": "LangGraph is a framework for building stateful AI workflows...",
  "sources": [
    "documents/langgraph_docs.txt"
  ]
}
```

---

## POST /ingest

Re-index all documents inside the `documents/` folder.

---

## GET /documents

Returns all indexed document names.

---

## POST /feedback

Stores user feedback for generated responses.

---

# Document Corpus

The knowledge base contains documentation for:

- LangChain
- LangGraph
- FastAPI
- ChromaDB
- Pydantic

Documents are stored inside the `documents/` directory and indexed into ChromaDB.

---

# Design Decisions & Tradeoffs

### Why LangGraph?

LangGraph was chosen to build a structured workflow with conditional routing, making it easy to manage retrieval, grading, retries, and answer generation.

### Why ChromaDB?

ChromaDB provides a lightweight persistent vector database suitable for semantic search without requiring external services.

### Why Sentence Transformers?

The `all-MiniLM-L6-v2` embedding model provides good semantic retrieval quality while remaining lightweight and fast.

### Why Query Rewriting?

Rewriting user queries improves retrieval quality by making search queries more descriptive and easier to match with indexed documents.

### Why Document Grading?

Retrieved documents may not always be relevant. An LLM-based grading step filters out irrelevant chunks before answer generation.

### Tradeoffs

- Prioritized simplicity and readability over adding advanced RAG techniques.
- Used a lightweight embedding model for faster local inference.
- Focused on a modular workflow that is easy to understand and extend.

---

# Thought Process

The goal was to build a modular RAG system where each stage of the pipeline has a single responsibility.

The workflow first improves the user query, retrieves relevant document chunks, filters irrelevant information, and finally generates a grounded response using only the retrieved context.

This design makes the pipeline easier to debug, understand, and extend with additional retrieval or grading strategies in the future.

---

# Chunking & Embedding Strategy

## Chunking

- RecursiveCharacterTextSplitter
- Chunk Size: **500**
- Chunk Overlap: **50**

This configuration balances retrieval accuracy while preserving context between chunks.

## Embedding Model

```
all-MiniLM-L6-v2
```

Chosen because it is lightweight, efficient, and performs well for semantic similarity tasks.

---

# Future Improvements

- PDF document support
- HTML document ingestion
- Hybrid keyword + semantic search
- Multi-document collections
- Conversation memory
- Authentication
- Support for additional embedding models

---

# Assumptions

- Documents are available locally inside the `documents/` directory.
- Users provide technical questions related to the indexed documentation.
- The Groq API key is configured before running the application.

---

# Acknowledgements

- LangChain
- LangGraph
- FastAPI
- ChromaDB
- Sentence Transformers
- Groq