from fastapi import FastAPI
from pydantic import BaseModel

from prompts import build_review_prompt
from reviewer import review_code


app = FastAPI(title="AI Code Reviewer")


class CodeInput(BaseModel):
    """Request body schema for code review requests."""

    code: str


@app.get("/")
def read_root() -> dict:
    """Health-check endpoint to verify the API is running."""

    return {"message": "AI Code Reviewer running"}


@app.post("/review-code")
def review_code_endpoint(payload: CodeInput) -> dict:
    """
    Accept source code, build an AI review prompt, send it to the local
    Ollama model, and return the AI-generated review text.
    """

    prompt = build_review_prompt(payload.code)
    review_text = review_code(prompt)
    return {"review": review_text}

