# AI Code Reviewer

AI Code Reviewer lets you paste or upload code and get an AI‑generated review using a local Ollama model (default: `llama3`) via a simple chat‑style UI.

## AI Model Architecture

This project uses a local Large Language Model (LLM) to analyze code and generate review suggestions.  
The model runs locally using Ollama with models such as `llama3`.

Using a local model provides several advantages:

- **Privacy:** Source code stays on the developer’s machine and is not sent to external APIs.
- **No API Costs:** The system does not depend on paid AI services.
- **Offline Capability:** Once the model is downloaded, the tool can run without internet access.

The architecture is designed to be **model-agnostic**, meaning the local model can be replaced with a hosted LLM API in production environments if needed.

## Prerequisites

- **Node.js** (LTS recommended) for the frontend.
- **Python 3.10+** for the backend.
- **Ollama** installed and running locally:
  - Install from `https://ollama.ai`
  - Pull the model used by this app:

    ```bash
    ollama run llama3
    ```

  - Make sure the Ollama server is listening on `http://localhost:11434` (default).

---

## Backend – FastAPI + Ollama

```bash
cd backend
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Frontend – React + Vite

From the repo root:

```bash
cd frontend
npm install
npm run dev
```

By default Vite runs at `http://localhost:5173`.

The frontend expects the backend at `http://localhost:8000` and is CORS‑enabled for `localhost:5173`.

---

## How to use the app

1. **Start Ollama**

   Make sure Ollama is running and the `llama3` model is available:

   ```bash
   ollama run llama3
   ```

2. **Run the backend**

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Run the frontend**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Open the UI**

   Visit `http://localhost:5173` in your browser.

5. **Get a review**

   - Paste code into the editor **or** click **Upload file** and choose a source file.
   - Optionally pick a **Language** to guide the review.
   - Click **Review Code** and read the AI’s structured feedback on the right.
