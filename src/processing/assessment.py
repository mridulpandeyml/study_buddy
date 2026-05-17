import json
from src.processing.llm_layer import co, api_key

def generate_quiz(context, num_questions=3):
    """
    Generates a multiple choice quiz based on the context using Gemini.
    Returns a list of dictionaries with 'question', 'options', and 'answer'.
    """
    if not api_key:
        return []
        
    prompt = f"""Based on the following text, generate a quiz with {num_questions} multiple choice questions.
Return the output strictly as a JSON array of objects, where each object has:
- "question": the question text
- "options": an array of 4 possible string answers
- "answer": the exact string of the correct option

Text:
{context}

JSON Array:"""
    
    try:
        response = co.chat(
            model="command-a-03-2025",
            message=prompt
        )
        # Parse the JSON output (strip any markdown formatting if present)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        quiz_data = json.loads(text)
        return quiz_data
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []
