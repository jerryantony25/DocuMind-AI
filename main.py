from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from document_processor import (
    extract_text_from_pdf,
    create_chunks
)

from vector_database import (
    store_chunks,
    search_documents
)

from rag import ask_document


# ============================================================
# DOCUMIND AI APPLICATION
# ============================================================

app = FastAPI(
    title="DocuMind AI",
    description="Intelligent Document Analyst",
    version="1.0.0"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"

DOCUMENTS_DIR.mkdir(exist_ok=True)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "DocuMind AI API is running!"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# PDF UPLOAD
# ============================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Only PDF files are allowed."
        }

    file_path = DOCUMENTS_DIR / file.filename

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "success": True,
        "filename": file.filename,
        "message": "Document uploaded successfully!"
    }


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

@app.post("/extract/{filename}")
def extract_document_text(filename: str):

    file_path = DOCUMENTS_DIR / filename

    if not file_path.exists():

        return {
            "success": False,
            "message": "Document not found."
        }

    if not filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Only PDF files are supported."
        }

    pages = extract_text_from_pdf(file_path)

    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    return {
        "success": True,
        "filename": filename,
        "total_pages": len(pages),
        "total_characters": total_characters,
        "pages": pages
    }


# ============================================================
# TEXT CHUNKING
# ============================================================

@app.post("/chunk/{filename}")
def chunk_document(filename: str):

    file_path = DOCUMENTS_DIR / filename

    if not file_path.exists():

        return {
            "success": False,
            "message": "Document not found."
        }

    if not filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Only PDF files are supported."
        }

    # Extract text
    pages = extract_text_from_pdf(
        file_path
    )

    # Create chunks
    chunks = create_chunks(
        pages
    )

    return {
        "success": True,
        "filename": filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "chunks": chunks
    }


# ============================================================
# STORE DOCUMENT IN CHROMADB
# ============================================================

@app.post("/store/{filename}")
def store_document(filename: str):

    file_path = DOCUMENTS_DIR / filename

    if not file_path.exists():

        return {
            "success": False,
            "message": "Document not found."
        }

    if not filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Only PDF files are supported."
        }

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    pages = extract_text_from_pdf(
        file_path
    )

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = create_chunks(
        pages
    )

    # --------------------------------------------------------
    # Store chunks and embeddings
    # --------------------------------------------------------

    result = store_chunks(
        filename,
        chunks
    )

    return result


# ============================================================
# SEMANTIC DOCUMENT SEARCH
# ============================================================

@app.get("/search")
def search_documents_api(
    query: str,
    top_k: int = 5
):

    return search_documents(
        query,
        top_k
    )


# ============================================================
# ASK DOCUMIND AI — GROK RAG
# ============================================================

@app.get("/ask")
def ask_document_api(
    question: str,
    top_k: int = 5
):

    return ask_document(
        question,
        top_k
    )