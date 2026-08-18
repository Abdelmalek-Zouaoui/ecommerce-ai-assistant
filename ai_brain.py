"""
ai_brain.py — Claude AI client & agent loop
Owner: MALEK

This is the AI brain. It receives a question and a store_id,
talks to Claude (with tools), and returns a text answer.

CONTRACT (agreed in Step 0 — do not change without telling Amine):
    ai_brain(question: str, store_id: str) -> str
"""

# TODO M1: Set up the Anthropic client and get a plain answer from Claude
# TODO M2: Register search_products as a tool Claude can call
# TODO M3: Register get_order_status as a tool Claude can call
# TODO M4: Write the system prompt (friendly, never invent data)


def ai_brain(question: str, store_id: str) -> str:
    """
    The ONE function Amine's server calls.

    Args:
        question:  what the customer asked (e.g. "Do you have red shirts?")
        store_id:  which store this is for (e.g. "store_a")

    Returns:
        A text answer to show the customer.
    """
    # TODO: replace with real Claude implementation
    raise NotImplementedError("Malek has not implemented this yet")
