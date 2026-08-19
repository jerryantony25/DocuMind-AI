from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Create vectorstore directory if it doesn't exist
VECTORSTORE_DIR.mkdir(exist_ok=True)


# ============================================================
# EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully.")


# ============================================================
# CHROMADB CLIENT
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)


# ============================================================
# DOCUMENT COLLECTION
# ============================================================

collection = chroma_client.get_or_create_collection(
    name="documind_documents",
    metadata={
        "description": "DocuMind AI document knowledge base"
    }
)


# ============================================================
# STORE DOCUMENT CHUNKS
# ============================================================

def store_chunks(filename: str, chunks: list):

    if not chunks:
        return {
            "success": False,
            "filename": filename,
            "chunks_stored": 0,
            "message": "No text chunks found."
        }

    documents = []
    embeddings = []
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        text = chunk["text"].strip()
        page = chunk["page"]

        # Skip empty chunks
        if not text:
            continue

        # ----------------------------------------------------
        # CREATE EMBEDDING
        # ----------------------------------------------------

        embedding = embedding_model.encode(
            text,
            convert_to_numpy=True
        ).tolist()

        # ----------------------------------------------------
        # STORE DOCUMENT DATA
        # ----------------------------------------------------

        documents.append(text)

        embeddings.append(embedding)

        ids.append(
            f"{filename}_{index}"
        )

        metadatas.append({
            "filename": filename,
            "page": page,
            "chunk_index": index
        })

    # --------------------------------------------------------
    # SAVE TO CHROMADB
    # --------------------------------------------------------

    if documents:

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    return {
        "success": True,
        "filename": filename,
        "chunks_stored": len(documents),
        "message": "Document chunks stored successfully."
    }


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(query: str, top_k: int = 5):

    # Make sure query is not empty
    if not query.strip():

        return {
            "success": False,
            "message": "Search query cannot be empty."
        }

    # --------------------------------------------------------
    # CREATE QUERY EMBEDDING
    # --------------------------------------------------------

    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    ).tolist()

    # --------------------------------------------------------
    # SEARCH CHROMADB
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    return {
        "success": True,
        "query": query,
        "results": results
    }


# ============================================================
# COLLECTION INFORMATION
# ============================================================

def get_collection_count():

    return collection.count()