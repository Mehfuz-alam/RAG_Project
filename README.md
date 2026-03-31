# RAG AI Assistant – Intelligent Document-Based Chat & Booking


**RAG AI Assistant** is a full-featured backend system built for multi-turn conversational AI over uploaded documents, with integrated interview booking. The project demonstrates proficiency in **FastAPI, NLP, Vector Databases, Redis, and LLM integration**, packaged with a modular, scalable, and production-ready architecture.

---

## 🚀 Features

### 📄 Document Ingestion

- Upload `.pdf` or `.txt` files via REST API.
- Extract text and clean it for NLP processing.
- Supports **two chunking strategies**:
  - Fixed-length chunks
  - Semantic paragraphs
- Generate embeddings using **SentenceTransformers**.
- Store embeddings in **Pinecone** vector database.
- Save document metadata in **PostgreSQL**.

### 💬 Conversational RAG API

- Custom **RAG (Retrieval-Augmented Generation)** implementation without RetrievalQAChain.
- Multi-turn conversations with **session-based memory** using **Redis**.
- Handles **context-aware responses** using previously uploaded documents.
- Supports **interview booking** by extracting:
  - Name
  - Email
  - Date & Time
- Booking info stored securely in **PostgreSQL**.

### ⚙️ Other Features

- Session-based isolation: multiple users can have separate document contexts.
- Fully modular, production-ready backend.
- Easy to extend with new LLMs or vector stores.

---

## 🏗️ Architecture Overview

```text
[User Frontend / Postman]
        |
        v
   FastAPI Backend
   ├─ /ingest (Document Upload)
   │   ├─ Text Extraction
   │   ├─ Chunking (Fixed/Semantic)
   │   ├─ Embedding Generation
   │   └─ Pinecone Vector Store + PostgreSQL
   ├─ /chat (Conversational RAG)
   │   ├─ Retrieve relevant embeddings from Pinecone
   │   ├─ Combine with Redis session memory
   │   ├─ Generate response using LLM (Gemini API)
   │   └─ Store multi-turn chat context in Redis
   └─ Booking Service
       ├─ Extract booking info via LLM
       └─ Store bookings in PostgreSQL
```

---

## 🛠️ Tech Stack

| Layer | Technology / Library |
|---|---|
| Backend Framework | FastAPI |
| NLP / Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Vector Database | Pinecone |
| Database | PostgreSQL |
| Chat Memory | Redis |
| LLM | Google Gemini API (`gemini-2.5-flash`) |
| PDF Processing | PyPDF |
| Containerization (optional) | Docker |
| Frontend (optional) | HTML/CSS/JS (for demo purposes) |

---

## 📦 Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/Mehfuz-alam/RAG_Project.git
cd RAG_Project
cd backend
```

**2. Create `.env` file with:**

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
GEMINI_API_KEY=your_gemini_api_key
REDIS_HOST=localhost
DB_URL=postgresql://user:password@localhost:5432/yourdb
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start backend**

```bash
uvicorn main:app --reload
```

**5. Visit API documentation**

```
http://127.0.0.1:8000/docs
```

---

## 🖼️ Demo Images

| Frontend UI | Postman Testing |
|---|---|
| ![Frontend UI](./assets/frontend.png) | <img width="959" height="503" alt="image" src="https://github.com/user-attachments/assets/6da8ac1e-52a1-409d-a563-6bb7d0abbb35" />
 |

| PostgreSQL Database | Docker / Redis Setup |
|---|---|
| ![PostgreSQL Database](./assets/postgres.png) | ![Docker / Redis Setup](./assets/docker.png) |

---

## 💡 How to Use

### 1. Upload a Document

1. Select a PDF or TXT file.
2. Choose chunking strategy (`fixed` or `semantic`).
3. Provide or auto-generate a `session_id`.
4. Click **Upload**.

### 2. Chat / Ask Questions

1. Use the same `session_id` as your uploaded document.
2. Type your question or booking request in the input box.
3. Receive context-aware answers from the AI.
4. Booking info is stored automatically if detected.

---

## 📝 Code Highlights

- **Modular Services:** `BookingService`, `IngestService`, `RAGService`.
- **Custom RAG:** fetch embeddings → construct prompt → generate response.
- **Redis memory:** session-based multi-turn chat stored as JSON.
- **Database models:** SQLAlchemy `Booking` and `Document` tables.

---

## 🌟 Key Learnings & Skills Demonstrated

- Implemented RAG pipeline from scratch (embedding + retrieval + LLM generation).
- Integrated vector DB (Pinecone) and Redis for session memory.
- Designed modular, clean Python services suitable for production.
- Applied LLM prompts for structured data extraction (interview booking).
- Learned to handle multi-turn conversational AI use cases.

---

## 📈 Future Improvements

- Add user authentication & session management.
- Improve booking extraction with more robust NLP parsing.
- Extend vector database support (Weaviate, Milvus, Qdrant).
- Add Docker Compose setup for full stack deployment.

---

## 📂 Project Structure

```
backend/
├─ app/
│  ├─ api/
│  │  ├─ routes_chat.py
│  │  └─ routes_ingest.py
│  ├─ services/
│  │  ├─ booking_service.py
│  │  ├─ ingest_service.py
│  │  └─ rag_service.py
│  ├─ llm/
│  │  ├─ embeddings_provider.py
│  │  └─ llm_provider.py
│  ├─ memory/redis_memory.py
│  ├─ vectorstore/pinecone_store.py
│  ├─ rag/chunking.py
│  ├─ db/
│  │  ├─ base.py
│  │  ├─ models.py
│  │  ├─ repositories.py
│  │  └─ session.py
│  └─ utils/
│     ├─ pdf_utils.py
│     └─ text_utils.py
├─ main.py
└─ requirements.txt
```

---

## 🔗 Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pinecone](https://www.pinecone.io/)
- [Redis](https://redis.io/)
- [SentenceTransformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)

---

> **Author:** Mehfuz Alam 
> **Date:** 2026
