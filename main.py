"""
main.py — FastAPI app & /chat endpoint
Owner: AMINE

The server receives questions from store websites and returns AI answers.

REQUEST:  POST /chat  { "question": "...", "api_key": "sk_store_a" }
RESPONSE:                { "answer": "..." }
"""

from fastapi import FastAPI, Body, HTTPException
from keys import get_store_id

app = FastAPI()

# --- A2: Fake AI brain (Malek's real version replaces this on join day) ---
def ai_brain(question, store_id):
    return f"[FAKE] You asked: {question} for store {store_id}"

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
