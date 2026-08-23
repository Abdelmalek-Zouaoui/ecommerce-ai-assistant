"""
main.py — FastAPI app & /chat endpoint
Owner: AMINE

The server receives questions from store websites and returns AI answers.

REQUEST:  POST /chat  { "question": "...", "api_key": "sk_store_a" }
RESPONSE:                { "answer": "..." }
"""

from pathlib import Path

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from keys import get_store_id
from ai_brain import ai_brain

app = FastAPI()

# Allow requests from the static ui.html (file://) and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serve the chat UI at the root URL."""
    html_path = Path(__file__).parent / "ui.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.post("/chat")
def chat(request: dict = Body()):
    # A3: Validate inputs
    question = request.get("question")
    api_key = request.get("api_key")

    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question'")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing 'api_key'")

    # A3: Check API key → which store?
    store_id = get_store_id(api_key)
    if not store_id:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # A2: Get AI answer
    answer = ai_brain(question, store_id)

    return {"answer": answer}
