# 🧠 DocuMind AI — RAG-Powered Intelligent Document Analysis System

> **An intelligent document analysis system that combines Retrieval-Augmented Generation (RAG), semantic search, vector databases, and Grok-4 to answer questions from uploaded PDF documents.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple)](https://www.trychroma.com/)
[![RAG](https://img.shields.io/badge/Architecture-RAG-orange)](#-how-it-works)
[![Grok](https://img.shields.io/badge/LLM-Grok--4-black)](https://x.ai/)

---

## 🚀 Overview

**DocuMind AI** is a Retrieval-Augmented Generation (RAG) based document intelligence system designed to allow users to upload PDF documents and ask questions about their content.

Instead of asking the LLM to answer from general knowledge, DocuMind AI first performs **semantic search over the uploaded document**, retrieves relevant chunks, and provides those chunks as context to **Grok-4** before generating the final answer.

This approach helps keep responses grounded in the uploaded documents and provides source information including the **document filename and page number**.

---

## ✨ Key Features

* 📄 **PDF Document Upload**
* 🔍 **PDF Text Extraction**
* ✂️ **Intelligent Text Chunking**
* 🧠 **Semantic Embeddings**
* 🗄️ **Persistent ChromaDB Vector Store**
* 🔎 **Semantic Document Search**
* 🤖 **Grok-4 LLM Integration**
* 📚 **Context-Aware Question Answering**
* 📌 **Source and Page-Aware Responses**
* ⚡ **FastAPI REST API**
* 🛡️ **Context-Grounded Responses**

---

## 🏗️ How It Works

```text
                  ┌─────────────────┐
                  │   Upload PDF    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │  Text Extraction│
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │  Text Chunking  │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │    Embeddings   │
                  │ MiniLM-L6-v2    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │    ChromaDB     │
                  │  Vector Store   │
                  └────────┬────────┘
                           ↓
             ┌──────────────────────────┐
             │    Semantic Retrieval    │
             └────────────┬─────────────┘
                          ↓
                  ┌─────────────────┐
                  │ Relevant Chunks │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │     Grok-4      │
                  │      LLM        │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │  Grounded AI    │
                  │     Answer      │
                  └─────────────────┘
```

---

## 🔄 RAG Pipeline

### 1. PDF Upload

Users upload a PDF document through the FastAPI `/upload` endpoint.

### 2. Text Extraction

DocuMind AI extracts text from every page using **PyPDF**.

### 3. Text Chunking

Extracted text is divided into smaller chunks using `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk Size:    1000
Chunk Overlap: 150
```

### 4. Embedding Generation

Each document chunk is converted into a semantic vector using:

```text
all-MiniLM-L6-v2
```

### 5. Vector Storage

The generated embeddings and document metadata are stored in **ChromaDB**.

Metadata includes:

* Filename
* Page number
* Chunk index

### 6. Semantic Search

When a user asks a question, the question is converted into an embedding and compared against the stored document vectors.

### 7. Context Construction

The most relevant document chunks are collected and combined into a context containing source information.

### 8. Grok-4 Generation

The retrieved context and user's question are passed to **Grok-4** through the xAI API.

The model is instructed to answer using the provided document context and avoid inventing information.

### 9. Source-Aware Response

The final response includes the answer along with the relevant document filename and page information.

---

## 🛠️ Tech Stack

| Technology                   | Purpose                         |
| ---------------------------- | ------------------------------- |
| **Python**                   | Core programming language       |
| **FastAPI**                  | REST API backend                |
| **PyPDF**                    | PDF text extraction             |
| **LangChain Text Splitters** | Document chunking               |
| **Sentence Transformers**    | Semantic embeddings             |
| **ChromaDB**                 | Vector database                 |
| **xAI API**                  | LLM integration                 |
| **Grok-4**                   | Answer generation               |
| **python-dotenv**            | Environment variable management |

---

## 📁 Project Structure

```text
DocuMind-AI/
│
├── main.py
├── document_processor.py
├── vector_database.py
├── rag.py
├── llm.py
├── .env
│
├── documents/
└── vectorstore/
```

### `main.py`

Contains the FastAPI application and REST endpoints.

### `document_processor.py`

Handles:

* PDF text extraction
* Page processing
* Text chunking

### `vector_database.py`

Handles:

* Sentence Transformer embeddings
* ChromaDB initialization
* Document storage
* Semantic search

### `rag.py`

Connects document retrieval with the LLM generation pipeline.

### `llm.py`

Handles:

* xAI API configuration
* Grok-4 requests
* Context-aware answer generation

---

## ⚡ Installation

### 1. Clone the repository

```bash
git clone https://github.com/jerryantony25/DocuMind-AI.git
cd DocuMind-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn python-multipart python-dotenv openai pypdf langchain-text-splitters chromadb sentence-transformers
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project directory:

```env
XAI_API_KEY=your_xai_api_key_here
```

> ⚠️ **Never commit your real API key to GitHub.**

Add `.env` to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

| Method | Endpoint              | Purpose                                |
| ------ | --------------------- | -------------------------------------- |
| `GET`  | `/`                   | Check application status               |
| `GET`  | `/health`             | Health check                           |
| `POST` | `/upload`             | Upload a PDF                           |
| `POST` | `/extract/{filename}` | Extract PDF text                       |
| `POST` | `/chunk/{filename}`   | Create document chunks                 |
| `POST` | `/store/{filename}`   | Generate embeddings and store document |
| `GET`  | `/search`             | Perform semantic search                |
| `GET`  | `/ask`                | Ask questions using the RAG pipeline   |

---

## 🧪 Example Workflow

### Upload a document

```text
POST /upload
```

Upload:

```text
example.pdf
```

### Store the document

```text
POST /store/example.pdf
```

The system processes the document through:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

### Ask a question

```text
GET /ask
```

Example:

```text
question=What is the main purpose of this document?
top_k=5
```

The system retrieves relevant chunks from ChromaDB and sends them as context to Grok-4.

---

## 💡 Example Response

```json
{
  "success": true,
  "question": "What is the main purpose of this document?",
  "answer": "The document explains ...",
  "sources": [
    {
      "filename": "example.pdf",
      "page": 3
    }
  ]
}
```

---

## 🎯 Why RAG?

Traditional LLM applications can generate answers based on their general training knowledge.

DocuMind AI follows a different approach:

```text
User Question
      ↓
Semantic Search
      ↓
Relevant Document Chunks
      ↓
Context
      ↓
Grok-4
      ↓
Grounded Answer
```

This allows the system to focus its responses on information retrieved from the uploaded documents.

---

## 🧠 Core AI Concepts Demonstrated

This project demonstrates practical implementation of:

* **Retrieval-Augmented Generation (RAG)**
* **Large Language Models (LLMs)**
* **Semantic Search**
* **Vector Embeddings**
* **Vector Databases**
* **Document Processing**
* **Context Retrieval**
* **Prompt Engineering**
* **REST API Development**
* **AI Application Architecture**

---

## 📌 Project Highlights

### 🔹 Document Intelligence

Transforms unstructured PDF content into searchable knowledge.

### 🔹 Semantic Retrieval

Uses embeddings instead of simple keyword matching to find relevant document content.

### 🔹 RAG Architecture

Retrieves relevant context before generating an answer.

### 🔹 Source Awareness

Maintains filename and page metadata during retrieval.

### 🔹 LLM Integration

Uses Grok-4 through the xAI API for final answer generation.

---

## 🔮 Future Enhancements

Potential improvements for future versions include:

* 🌐 Web-based frontend
* 👥 Multi-user document management
* 📚 Multiple document collections
* 💬 Conversational chat history
* 📊 Document analytics dashboard
* 🔐 Authentication and authorization
* 🧾 Support for DOCX and TXT files
* 📈 Retrieval evaluation and RAG metrics
* ☁️ Cloud deployment
* 🐳 Docker containerization
* ⚡ Streaming LLM responses
* 🧠 Advanced reranking
* 🔄 Background document processing

---

## ⚠️ Security

Never expose your xAI API key in:

* GitHub repositories
* Screenshots
* LinkedIn posts
* README files
* Frontend code

Use environment variables instead:

```env
XAI_API_KEY=your_xai_api_key_here
```

---

## 👨‍💻 Author

### Jerry Antony S

**B.Sc. Artificial Intelligence & Machine Learning**

Interested in:

**Generative AI • LLMs • RAG • Machine Learning • AI Engineering • Full-Stack AI**

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is intended for educational and development purposes.
