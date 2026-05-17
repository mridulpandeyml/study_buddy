import os
import cohere

# Try to load env if available
from dotenv import load_dotenv
load_dotenv()

# Configure Cohere
api_key = os.getenv("COHERE_API_KEY")
co = None
if api_key:
    co = cohere.Client(api_key=api_key)

def generate_answer(query, context, mode="Standard"):
    """
    Generates an answer based on the provided query and context using Cohere.
    Adjusts tone based on mode.
    """
    if not co:
        return "API Key not found. Please set COHERE_API_KEY in your .env file."
        
    system_prompt = f"""You are an expert AI tutor. Your goal is to answer the student's question based strictly on the provided context.
If the context does not contain the answer, say "I don't have enough information to answer that based on the uploaded documents."
Current difficulty mode: {mode}.
- If Beginner: Explain simply, use analogies, and avoid heavy jargon.
- If Standard: Give a clear, direct, college-level explanation.
- If Advanced: Dive deep into technical details, mechanisms, and edge cases.
"""

    prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    try:
        response = co.chat(
            model="command-a-03-2025",
            message=prompt
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Cohere API: {e}"
