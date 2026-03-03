import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

import pdfplumber

from services.difficulty_service import get_difficulty
from services.ai_service import generate_explanation, generate_quiz, generate_flashcard, analyze_pdf, generate_chat_reply

app = FastAPI(title="LearnLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    text: str              # The original highlighted text
    explanation: str       # The original explanation
    history: list          # Previous chat messages as [{"role": "user"/"assistant", "content": "..."}]
    question: str          # The new question the user is asking

@app.get("/")
def read_root():
    return {"status": "ok", "message": "LearnLens API is running."}

@app.post("/explain")
async def explain(request: TextRequest):
    difficulty = get_difficulty(request.text)
    explanation = await generate_explanation(request.text, difficulty["level"])
    return {
        "explanation": explanation,
        "level": difficulty["level"],
        "confidence": difficulty["confidence"]
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    reply = await generate_chat_reply(request.text, request.explanation, request.question, request.history)
    return {
        "reply": reply
    }

@app.post("/quiz")
async def quiz(request: TextRequest):
    difficulty = get_difficulty(request.text)
    quiz_data = await generate_quiz(request.text, difficulty["level"])
    return {
        "quiz": quiz_data,
        "level": difficulty["level"]
    }

@app.post("/flashcard")
async def flashcard(request: TextRequest):
    difficulty = get_difficulty(request.text)
    flashcard_data = await generate_flashcard(request.text, difficulty["level"])
    return {
        "flashcard": flashcard_data,
        "level": difficulty["level"]
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = ""
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
    except Exception as e:
        return {"error": "Failed to read PDF file format."}
    
    if not content.strip():
        return {"error": "Could not extract any text from this PDF. It might be an image-based or scanned document."}
    
    # Try to use the filename as the topic (remove .pdf)
    topic_name = os.path.splitext(file.filename)[0] if file.filename else "PDF Upload"
    
    word_count = len(content.split())
    # truncate content to a reasonable length for analysis if needed (e.g., first 5000 chars)
    analysis_text = content[:5000]
    
    difficulty = get_difficulty(analysis_text)
    analysis = await analyze_pdf(analysis_text, difficulty["level"], topic_name)
    
    return {
        "analysis": analysis,
        "level": difficulty["level"],
        "confidence": difficulty["confidence"],
        "word_count": word_count
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
