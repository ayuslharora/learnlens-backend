import os
import json
from groq import AsyncGroq

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
model = "llama-3.1-8b-instant"

async def generate_explanation(text: str, level: str) -> str:
    prompt = f"""
    You are an expert tutor. Explain the following text to a '{level}' level reader.
    Text: {text}
    """
    if level == "Beginner":
        prompt += " Use simple words, analogies, and real-life examples. Keep it concise."
    elif level == "Intermediate":
        prompt += " Provide moderate detail and explain any technical terms."
    else:
        prompt += " Use technical language and assume domain knowledge."

    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return response.choices[0].message.content

async def generate_quiz(text: str, level: str) -> dict:
    prompt = f"""
    You are an expert tutor. Based on the following text, generate a 4-option multiple-choice question suitable for a '{level}' level reader.
    Text: {text}
    
    Return ONLY a JSON object with this exact format, without markdown or extra text:
    {{
        "question": "Question text here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": "The exact text of the correct option",
        "explanation": "Why this option is correct."
    }}
    """
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

async def generate_flashcard(text: str, level: str) -> dict:
    prompt = f"""
    You are an expert tutor. Based on the following text, extract the most important concept and create a flashcard for a '{level}' level reader.
    Text: {text}
    
    Return ONLY a JSON object with this exact format, without markdown or extra text:
    {{
        "front": "Question or key term",
        "back": "Answer or definition",
        "topic": "One word topic (e.g. biology, physics)"
    }}
    """
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

async def analyze_pdf(text: str, level: str, topic: str) -> dict:
    prompt = f"""
    You are an expert tutor. Analyze the following document text and extract the most important facts, definitions, and concepts to create a comprehensive deck of flashcards suitable for a '{level}' level reader.
    Text: {text[:5000]}
    
    You must generate between 10 and 20 flashcards depending on the length of the text.
    You MUST use the exact string "{topic}" for the "topic" field on every single flashcard.
    
    Return ONLY a JSON object with this exact format, containing an array called "flashcards":
    {{
        "flashcards": [
            {{
                "front": "Question or key term",
                "back": "Answer or definition",
                "topic": "{topic}"
            }},
            {{
                "front": "Another question",
                "back": "Another answer",
                "topic": "{topic}"
            }}
        ]
    }}
    """
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
