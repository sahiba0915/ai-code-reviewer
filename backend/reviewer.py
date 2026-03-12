import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def review_code(prompt: str) -> str:
    """
    Send the review prompt to the local Ollama instance and return the
    model's response text.

    This function isolates all LLM / HTTP details from the API layer.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    # The Ollama API returns the generated text in the "response" field
    # when streaming is disabled.
    return data.get("response", "").strip()

