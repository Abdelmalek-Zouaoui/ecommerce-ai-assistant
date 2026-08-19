"""
main.py — FastAPI app & /chat endpoint
Owner: AMINE

The server receives questions from store websites and returns AI answers.

REQUEST:  POST /chat  { "question": "...", "api_key": "sk_store_a" }
RESPONSE:                { "answer": "..." }
"""

# TODO A1: Create the FastAPI app
# TODO A2: Create the /chat endpoint that calls ai_brain()
# TODO A3: Validate api_key on every request (use keys.py)
# TODO A4: Load store data (use data.py)
from fastapi import FastAPI, Body

app = FastAPI()
@app.post("/chat")
def chat(request: dict = Body()):
    return {"answer":request["question"]} 

    