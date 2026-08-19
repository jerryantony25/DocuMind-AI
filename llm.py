import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")


if not XAI_API_KEY:
    raise ValueError(
        "XAI_API_KEY is missing from the .env file."
    )


# ============================================================
# GROK CLIENT
# ============================================================

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question: str, context: str):

    prompt = f"""
You are DocuMind AI, an intelligent document analysis assistant.

Answer the user's question using ONLY the information
provided in the document context.

If the answer cannot be found in the context, say:

"I could not find this information in the uploaded documents."

Do not invent information.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are DocuMind AI, a document "
                    "analysis assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content