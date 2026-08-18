"""
ai_brain.py — Groq AI client & agent loop
Owner: MALEK

This is the AI brain. It receives a question and a store_id,
talks to Groq (with tools), and returns a text answer.

CONTRACT (agreed in Step 0 — do not change without telling Amine):
    ai_brain(question: str, store_id: str) -> str
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import get_order_status, search_products

load_dotenv()

client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url="https://api.groq.com/openai/v1")
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are a friendly customer support assistant for an online store.

Rules:
- NEVER invent prices, stock levels, or order information. Only state facts returned
  by the search_products or get_order_status tools.
- If a tool returns no match, say so plainly and offer to connect the customer to
  human support instead of guessing.
- Keep answers short, direct, and warm.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search this store's product catalog by name, description, or category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search text, e.g. 'red shirt' or 'shoes'"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up the status of a specific order by its order id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order id, e.g. '101'"},
                },
                "required": ["order_id"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "search_products": search_products,
    "get_order_status": get_order_status,
}


def ai_brain(question: str, store_id: str) -> str:
    """
    The ONE function Amine's server calls.

    Args:
        question:  what the customer asked (e.g. "Do you have red shirts?")
        store_id:  which store this is for (e.g. "store_a")

    Returns:
        A text answer to show the customer.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or ""

        messages.append(message)

        for tool_call in message.tool_calls:
            func = TOOL_FUNCTIONS[tool_call.function.name]
            args = json.loads(tool_call.function.arguments)
            result = func(store_id, **args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    return "Sorry, I couldn't finish looking that up. Let me connect you to support."
