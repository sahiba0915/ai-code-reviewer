import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from prompts import build_review_prompt  # type: ignore
    from reviewer import review_code, review_structured  # type: ignore
    from schema import CodeReviewResult  # type: ignore
except ModuleNotFoundError:
    from backend.prompts import build_review_prompt  # type: ignore
    from backend.reviewer import review_code, review_structured  # type: ignore
    from backend.schema import CodeReviewResult  # type: ignore


app = FastAPI(title="AI Code Reviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeInput(BaseModel):
    """Request body schema for code review requests."""

    code: str
    language: str | None = None


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
    try:
        prompt = build_review_prompt(payload.code, payload.language)
        review_text = review_code(prompt)
        return {"review": review_text}
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start it with 'ollama serve', then run 'ollama run llama3'.",
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond. Try again or use a smaller code snippet.",
        )
    except requests.exceptions.HTTPError as e:
        msg = "Ollama error."
        if e.response is not None and e.response.status_code == 404:
            msg = "Model 'llama3' not found. Run 'ollama run llama3' to download it."
        raise HTTPException(status_code=503, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/review-structured", response_model=CodeReviewResult)
def review_structured_endpoint(payload: CodeInput) -> CodeReviewResult:
    try:
        return review_structured(code=payload.code, language=payload.language, file_label="pasted_code")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start it with 'ollama serve', then run 'ollama run llama3'.",
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond. Try again or use a smaller code snippet.",
        )
    except requests.exceptions.HTTPError as e:
        msg = "Ollama error."
        if e.response is not None and e.response.status_code == 404:
            msg = "Model 'llama3' not found. Run 'ollama run llama3' to download it."
        raise HTTPException(status_code=503, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

