from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from .ai_pipeline import run_ai_pipeline

app = FastAPI(title="Review Analytics AI Backend")

class ReviewRequest(BaseModel):
    text: str
    rating: int
    userId: Optional[str] = None

@app.post("/analyze")
async def analyze_review(request: ReviewRequest):
    return await run_ai_pipeline(request.text, request.rating, request.userId)
