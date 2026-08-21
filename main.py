"""
main.py — FastAPI app & /chat endpoint
Owner: AMINE

The server receives questions from store websites and returns AI answers.

REQUEST:  POST /chat  { "question": "...", "api_key": "sk_store_a" }
RESPONSE:                { "answer": "..." }
"""

from fastapi import FastAPI, Body, HTTPException

from ai_brain import ai_brain
from keys import get_store_id

app = FastAPI()


@app.post("/chat")
def chat(request: dict = Body()):
    question = request.get("question")
    api_key = request.get("api_key")

    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question'")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing 'api_key'")

    store_id = get_store_id(api_key)
    if not store_id:
        raise HTTPException(status_code=401, detail="Invalid API key")

    answer = ai_brain(question, store_id)

    return {"answer": answer}
