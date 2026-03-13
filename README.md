<p align="center">
  <h1 align="center">Mini RAG</h1>
  <p align="center">
    <strong>A lightweight, modular Retrieval-Augmented Generation (RAG) API built with FastAPI</strong>
  </p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#api-reference">API Reference</a> •
    <a href="#configuration">Configuration</a>
  </p>
</p>

---

## 📖 Overview

**Mini RAG** is a personal project that implements a complete RAG (Retrieval-Augmented Generation) pipeline as a RESTful API. It allows you to upload documents, process them into semantic chunks, store embeddings in a vector database, and perform similarity searches to retrieve relevant context for AI-powered applications.

Built with a clean, modular architecture—this project demonstrates production-ready patterns including factory design patterns for LLM providers, async database operations, and containerized infrastructure.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Document Processing** | Upload and process PDF, DOCX, and TXT files with configurable chunking |
| 🔍 **Semantic Search** | Vector similarity search using embeddings for intelligent document retrieval |
| 🔌 **Pluggable LLM Providers** | Factory pattern supporting Ollama and Cohere (easily extensible) |
| 🗄️ **Vector Database** | Qdrant integration for high-performance vector storage and search |
| 📊 **Project Management** | Organize documents and indexes by project for multi-tenant use cases |
| 🐳 **Docker Ready** | MongoDB containerized for easy local development |
| ⚡ **Async First** | Built on FastAPI with async MongoDB operations (Motor) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI App                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │   Routes    │   │ Controllers │   │   Models    │          │
│   │  ─────────  │──▶│  ─────────  │──▶│  ─────────  │          │
│   │  • base     │   │  • Data     │   │  • Project  │          │
│   │  • data     │   │  • NLP      │   │  • Asset    │          │
│   │  • nlp      │   │  • Process  │   │  • Chunk    │          │
│   └─────────────┘   └─────────────┘   └─────────────┘          │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                      Stores                              │  │
│   │  ┌──────────────────────┐  ┌──────────────────────────┐ │  │
│   │  │     LLM Factory      │  │   VectorDB Factory       │ │  │
│   │  │  ────────────────    │  │  ──────────────────      │ │  │
│   │  │  • Ollama Provider   │  │  • Qdrant Provider       │ │  │
│   │  │  • Cohere Provider   │  │                          │ │  │
│   │  └──────────────────────┘  └──────────────────────────┘ │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
          │                               │
          ▼                               ▼
    ┌───────────┐                  ┌────────────┐
    │  MongoDB  │                  │   Qdrant   │
    │  (Motor)  │                  │ VectorDB   │
    └───────────┘                  └────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MongoDB (via Docker or local installation)
- Qdrant vector database
- Ollama (for local LLM inference) or Cohere API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mini-rag.git
   cd mini-rag
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. **Start MongoDB with Docker**
   ```bash
   cd docker
   docker-compose up -d
   ```

5. **Configure environment variables**
   ```bash
   cd src
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

---

## 📚 API Reference

### Base Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check - returns app name and version |

### Data Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/data/upload/{project_id}` | Upload files to a project |
| `POST` | `/data/process/{project_id}` | Process files into chunks |

### NLP Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/nlp/index/push/{project_id}` | Index document chunks into vector DB |
| `GET` | `/nlp/index/info/{project_id}` | Get vector collection info |
| `POST` | `/nlp/index/search/{project_id}` | Semantic search across indexed documents |

### Example: Upload and Search Flow

```bash
# 1. Upload a document
curl -X POST "http://localhost:8000/data/upload/my-project" \
  -F "file=@document.pdf"

# 2. Process the document into chunks
curl -X POST "http://localhost:8000/data/process/my-project" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "...", "chunk_size": 100, "over_lap_size": 20}'

# 3. Index chunks into vector database
curl -X POST "http://localhost:8000/nlp/index/push/my-project" \
  -H "Content-Type: application/json" \
  -d '{"do_reset": false}'

# 4. Search for relevant content
curl -X POST "http://localhost:8000/nlp/index/search/my-project" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is machine learning?", "limit": 5}'
```

---

## ⚙️ Configuration

Create a `.env` file in the `src` directory based on `.env.example`:

```env
# Application
APP_NAME="Mini RAG"
APP_VERSION="0.0.1"

# File Processing
FILE_ALLOWED_TYPES=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain"]
FILE_MAX_SIZE=10485760          # 10 MB
FILES_DEFAULT_CHUNK_SIZE=512000 # 500 KB

# Database
MONGODB_URL="mongodb://username:password@localhost:27017"
MONGODB_DB_NAME="mini_rag"

# LLM Configuration
GENERATION_BACKEND="ollama"     # or "cohere"
GENERATION_MODEL_ID="llama2"
EMBEDDING_BACKEND="ollama"
EMBEDDING_MODEL_ID="nomic-embed-text"
EMBEDDING_SIZE=768

# Vector Database
VECTOR_DB_PROVIDER="qdrant"
QDRANT_URL="http://localhost:6333"
```

---

## 📁 Project Structure

```
mini-rag/
├── docker/
│   ├── docker-compose.yml    # MongoDB container configuration
│   └── .env.example
├── src/
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── controllers/          # Business logic layer
│   │   ├── DataController.py
│   │   ├── NLPController.py
│   │   └── ProcessController.py
│   ├── routes/               # API endpoints
│   │   ├── base.py
│   │   ├── data.py
│   │   └── nlp.py
│   ├── models/               # Data models & schemas
│   │   ├── ProjectModel.py
│   │   ├── AssetModel.py
│   │   └── ChunkModel.py
│   ├── stores/               # External service integrations
│   │   ├── llm/              # LLM providers (Ollama, Cohere)
│   │   └── vectordb/         # Vector DB providers (Qdrant)
│   └── helpers/              # Utilities and config
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | FastAPI |
| **Database** | MongoDB (Motor async driver) |
| **Vector Store** | Qdrant |
| **LLM Providers** | Ollama, Cohere |
| **Document Processing** | LangChain, PyMuPDF |
| **Validation** | Pydantic |
| **Containerization** | Docker Compose |

---

## 🔮 Future Enhancements

- [ ] Add OpenAI provider support
- [ ] Implement RAG generation endpoint (query → retrieve → generate)
- [ ] Add authentication and API keys
- [ ] Create a simple web UI for document management
- [ ] Add support for more document formats (HTML, Markdown)
- [ ] Implement document deduplication
- [ ] Add caching layer for embeddings

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ as a personal project to explore RAG architectures
</p>