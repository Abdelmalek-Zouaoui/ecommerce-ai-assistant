# Plan — Day by Day

Picking up from the current state: Malek's `ai_brain.py`/`tools.py` are code-complete
(Groq, via the OpenAI-compatible API). Amine's `main.py`/`keys.py` are still empty stubs.

## Day 1 — Unblock & validate Malek's side ✅ DONE

- [x] Get a working API key and drop it into `.env`. (Originally planned for xAI/Grok;
      switched to **Groq** — a different, hosted, free-tier provider — since xAI's API
      requires paid credits. Same OpenAI-compatible code either way.)
- [x] Run `python test_ai.py`, confirm all 5 sample questions return sane answers
      (tool calls firing correctly for both `search_products` and `get_order_status`)
- [x] Sanity-check: asked for a nonexistent product ("hats") and a nonexistent order
      (#999) — both correctly said "not found" and offered human handoff, instead of
      guessing

## Day 2 — Prompt hardening (Malek) + server skeleton (Amine)

**Malek (M4): ✅ DONE — see [issue #2](https://github.com/Abdelmalek-Zouaoui/ecommerce-ai-assistant/issues/2) for the full writeup**
- [x] Tested far more than 10 edge-case questions: ambiguous/multi-match search,
      hallucination attempts, direct + indirect prompt injection, off-topic abuse,
      sensitive data, malformed store data, multi-language (incl. Arabic)
- [x] Tightened `SYSTEM_PROMPT` repeatedly based on real failures found, and made
      `tools.py` reject malformed store data instead of crashing

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

- [ ] Wrap the `ai_brain()` call in `main.py` in try/except so a Groq error/timeout
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
