from vector_database import search_documents
from llm import generate_answer


def ask_document(question: str, top_k: int = 5):

    # Search ChromaDB
    search_result = search_documents(
        question,
        top_k
    )

    if not search_result.get("success"):
        return {
            "success": False,
            "message": search_result.get(
                "message",
                "Search failed."
            )
        }

    results = search_result["results"]

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:
        return {
            "success": False,
            "message": "No relevant information found."
        }

    # Build context
    context_parts = []
    sources = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        filename = metadata.get(
            "filename",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"[Source: {filename}, Page {page}]\n"
            f"{document}"
        )

        sources.append({
            "filename": filename,
            "page": page
        })

    context = "\n\n".join(context_parts)

    # Ask Grok
    answer = generate_answer(
        question,
        context
    )

    return {
        "success": True,
        "question": question,
        "answer": answer,
        "sources": sources
    }