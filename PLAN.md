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

**Amine (A1–A2): ✅ DONE**
- [x] `main.py`: FastAPI app, `/chat` endpoint accepting `{question, api_key}`,
      returning `{answer}`
- [x] Wire it to the real `ai_brain()` directly (no need for a fake stub since it
      already works) — run with `uvicorn main:app --reload`, check `/docs`

(Merged from Amine's `amine/server-and-keys` branch, then swapped his fake
`ai_brain()` stub for the real import per the plan above.)

## Day 3 — Auth + join (Amine, Malek reviews) ✅ DONE

**Amine (A3–A4):**
- [x] `keys.py`: dict of `api_key → store_id`, reject unknown keys with a clear
      401/403
- [x] Confirm `data.py` (already implemented) matches expectations — flag if it
      needs changes (no changes needed)
- [x] Add a second store (`data/store_b/...`) to prove multi-tenant isolation
      actually works, not just single-store

**Together:**
- [x] End-to-end test: call `/chat` with `sk_store_a` and `sk_store_b`, confirm each
      only ever sees its own products/orders — see `test_multi_tenant.py`
      (11/11 checks passed, including the same order id "101" existing in both
      stores with different data)

## Day 4 — Hardening + external test ✅ DONE

- [x] Wrap the `ai_brain()` call in `main.py` in try/except so a Groq error/timeout
      returns a clean error response, not a 500 stack trace to the customer
      (returns 503 + logs the real exception server-side via `logger.exception`)
- [x] Test "from another site": a separate script or simple HTML page hitting the
      deployed/local `/chat` with an API key — see `examples/store_widget.html`,
      verified in a real browser. This surfaced a real bug: no CORS config meant
      every browser-based store integration would be silently blocked by the
      preflight check. Fixed with `CORSMiddleware(allow_origins=["*"])` — the
      `api_key` check is what actually gates data access, not the origin.
- [x] Edge cases: missing `api_key` (400), empty question string (400, `""` is
      falsy), malformed JSON / empty body (422, FastAPI's built-in validation —
      clean JSON, no stack trace). Left as FastAPI's default shape rather than
      normalizing to match our own `{"detail": "..."}` errors — noted as a minor,
      non-blocking inconsistency for a future pass.

## Day 5 (optional — only if Days 1–4 go smoothly) — Deploy

- [ ] Amine deploys to Render/Railway/Fly.io, sets `LLM_API_KEY` as a host secret
      (never commit it)
- [ ] Smoke-test the public URL with a real request
- [ ] Write a short README: how to add a new store (new API key + new
      `data/<store_id>/` folder)
