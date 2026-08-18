# Plan — Day by Day

Picking up from the current state: Malek's `ai_brain.py`/`tools.py` are code-complete
(Grok, via the OpenAI-compatible API), pending a valid API key. Amine's `main.py`/`keys.py`
are still empty stubs.

## Day 1 — Unblock & validate Malek's side

- [ ] Get the real `xai-...` key from console.x.ai, drop it into `.env`
- [ ] Run `python test_ai.py`, confirm all 5 sample questions return sane answers
      (tool calls firing correctly for both `search_products` and `get_order_status`)
- [ ] Sanity-check: ask something with no match (e.g. "do you have hats?") and confirm
      it says "no match" instead of guessing

## Day 2 — Prompt hardening (Malek) + server skeleton (Amine)

**Malek (M4):**
- [ ] Test ~10 more questions (ambiguous ones, multiple products matching, cancelled/
      delivered orders, nonexistent order id)
- [ ] Tighten `SYSTEM_PROMPT` based on what goes wrong (tone, refusing to invent data,
      handoff wording)

**Amine (A1–A2):**
- [ ] `main.py`: FastAPI app, `/chat` endpoint accepting `{question, api_key}`,
      returning `{answer}`
- [ ] Wire it to the real `ai_brain()` directly (no need for a fake stub since it
      already works) — run with `uvicorn main:app --reload`, check `/docs`

## Day 3 — Auth + join (Amine, Malek reviews)

**Amine (A3–A4):**
- [ ] `keys.py`: dict of `api_key → store_id`, reject unknown keys with a clear
      401/403
- [ ] Confirm `data.py` (already implemented) matches expectations — flag if it
      needs changes
- [ ] Add a second store (`data/store_b/...`) to prove multi-tenant isolation
      actually works, not just single-store

**Together:**
- [ ] End-to-end test: call `/chat` with `sk_store_a` and `sk_store_b`, confirm each
      only ever sees its own products/orders

## Day 4 — Hardening + external test

- [ ] Wrap the `ai_brain()` call in `main.py` in try/except so a Grok error/timeout
      returns a clean error response, not a 500 stack trace to the customer
- [ ] Test "from another site": a separate script or simple HTML page hitting the
      deployed/local `/chat` with an API key
- [ ] Edge cases: missing `api_key`, malformed JSON, empty question string

## Day 5 (optional — only if Days 1–4 go smoothly) — Deploy

- [ ] Amine deploys to Render/Railway/Fly.io, sets `LLM_API_KEY` as a host secret
      (never commit it)
- [ ] Smoke-test the public URL with a real request
- [ ] Write a short README: how to add a new store (new API key + new
      `data/<store_id>/` folder)
