"""
main.py — FastAPI app & /chat endpoint
Owner: AMINE

The server receives questions from store websites and returns AI answers.

REQUEST:  POST /chat  { "question": "...", "api_key": "sk_store_a" }
RESPONSE:                { "answer": "..." }
"""

import logging

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai_brain import ai_brain
from keys import get_store_id

logger = logging.getLogger(__name__)

app = FastAPI()

# Any store's website can call us from the browser — the api_key check below is
# what actually gates access to data, not the request's origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


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

    try:
        answer = ai_brain(question, store_id)
    except Exception:
        logger.exception("ai_brain() failed for store_id=%s", store_id)
        raise HTTPException(
            status_code=503,
            detail="We're having trouble answering right now. Please try again shortly.",
        )

    return {"answer": answer}
