"""
test_ai.py — Malek's standalone AI testing script
Owner: MALEK

Run with:  python test_ai.py
Tests the AI brain WITHOUT needing the FastAPI server running.
"""

from ai_brain import ai_brain

# Test questions — try these once ai_brain is implemented
test_questions = [
    ("Do you have red shirts?", "store_a"),
    ("What's the status of order 101?", "store_a"),
    ("Do you have any shoes in stock?", "store_a"),
    ("How much is the green hoodie?", "store_a"),
    ("Where is my order #104?", "store_a"),
]

if __name__ == "__main__":
    for question, store_id in test_questions:
        print(f"\n{'='*60}")
        print(f"Q: {question}  (store: {store_id})")
        print(f"{'='*60}")
        answer = ai_brain(question, store_id)
        print(f"A: {answer}")
