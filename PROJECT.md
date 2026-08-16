# E-commerce AI Assistant

A multi-tenant conversational AI assistant that e-commerce store owners integrate into
their own websites via an API key — similar in spirit to Intercom Fin / Tidio / Rep AI,
but focused on e-commerce use cases (product Q&A, recommendations, order support, FAQ).

Store owners buy an API key from us, drop a widget snippet (or call our REST API) into
their site, and their customers get an AI shopping assistant grounded in that store's
own product catalog and order data.

## 1. What we're building

Three moving pieces:

1. **Our platform** — tenant accounts, API keys, billing, dashboard, the AI brain.
2. **Integration surface** — how a store owner's website talks to our assistant (widget
   + API), regardless of what platform their store runs on.
3. **Data connectors** — how the assistant gets a *specific* store's products/orders,
   since every merchant's stack differs (Shopify, WooCommerce, custom).

## 2. Core architecture

```
Merchant's website
  └─ embeddable JS widget (<script src="ours.com/widget.js" data-key="pk_live_...">)
        │  REST/SSE calls
        ▼
API Gateway  ── validates API key, rate-limits, meters usage
        ▼
Conversation Orchestrator (Claude API, tool-calling agent)
   ├─ tool: search_products      → RAG over tenant's product catalog
   ├─ tool: get_recommendations  → RAG + purchase/browse signals
   ├─ tool: get_order_status     → calls tenant's Order Adapter
   └─ tool: escalate_to_human    → email/webhook to tenant support
        ▼
Adapter layer (per-platform)
   ├─ Shopify adapter     (Storefront API + Admin API)
   ├─ WooCommerce adapter (REST API + auth)
   └─ Generic adapter     (tenant's own webhook/REST endpoints, for custom sites)
        ▼
Tenant DB / vector store (namespaced per tenant)
```

Key principle: the agent never free-types facts about prices, stock, or orders — it
only reports what a tool call returns. This is what keeps the product from
confidently hallucinating a wrong order status to someone else's customer.

## 3. Best practices

- **Multi-tenant isolation**: every row tagged with `tenant_id`, enforced with Postgres
  row-level security, not just app-layer checks. One vector namespace per tenant —
  never let store A's assistant retrieve store B's products.
- **Secrets, not plaintext**: merchants hand us Shopify/Woo API tokens. Encrypt at rest
  (KMS/Vault), never log them, support revocation.
- **API keys**: prefix + hash at rest (`sk_live_...`), show the raw value once, support
  rotation without downtime.
- **Read vs write actions**: product Q&A/status checks are safe to automate; refunds and
  cancellations should either require tenant-side confirmation or route through the
  tenant's own system rather than the LLM calling a destructive endpoint directly.
- **RAG freshness**: catalogs change constantly — sync via webhook (order/product
  updated) or scheduled pull, don't assume a one-time import.
- **Prompt injection from our own data**: product descriptions/reviews are merchant- or
  customer-authored text that ends up in the model's context via RAG — treat it as
  untrusted input, not trusted instructions.
- **Usage metering from day one**: log tokens/calls per tenant even before charging for
  it — retrofitting billing math later is painful.
- **Human handoff path**: always give the assistant a documented "I can't help with
  this, here's how to reach support" exit.
- **Start with one integration path**: generic REST + JS widget first. Native
  Shopify/WooCommerce apps (App Store listings, OAuth install) are a phase-2
  distribution channel, not an MVP requirement.

## 4. Recommended stack

| Layer | Choice | Why |
|---|---|---|
| Language | TypeScript everywhere | One language across API, dashboard, widget |
| Backend | Node.js (Fastify) | Lightweight, good Claude SDK support, easy to deploy |
| DB + vector store | Supabase (Postgres + pgvector + auth) | Row-level security built in, avoids a separate vector DB early |
| LLM | Claude API — Sonnet for the agent, Haiku for cheap intent-routing | Tool-calling for grounded answers; Haiku keeps routing/classification cheap |
| Dashboard | Next.js | Tenant self-serve signup, API key management, catalog upload |
| Widget | Vanilla TS bundled with Vite, embeddable `<script>` | No framework lock-in for merchants |
| Jobs | BullMQ + Redis | Catalog sync, embedding generation, async webhook processing |
| Billing | Stripe (metered) | Usage-based pricing matches the per-API-call model |
| Hosting | Fly.io or Render | Simple ops for a 2-person team |

## 5. Team split

**Person A — Platform & Integrations**
Tenant/account model, API gateway (auth, rate limiting, key issuance), Stripe
billing/metering, Shopify adapter, secrets management, deployment/CI.

**Person B — AI & Product Experience**
Claude agent + tool-calling logic, RAG pipeline (embeddings, retrieval, catalog sync),
prompt design + eval set, embeddable widget UI/UX, conversation analytics.

**Shared**: data model design (tenants/products/orders/conversations schema), the
generic REST adapter (so custom-site merchants can integrate day one), security review
before launch.

## 6. Phasing

1. **Weeks 1–2**: Nail the API contract and data model. Decide what a "tool call"
   looks like for a merchant who has zero platform integration yet (generic REST).
2. **Weeks 3–6 (MVP)**: One hardcoded test tenant, generic connector, widget, Q&A + FAQ
   via RAG, product search tool. No order writes yet.
3. **Weeks 7–10**: Self-serve onboarding (dashboard, API key issuance, catalog
   CSV/API upload), order-status tool, usage metering + Stripe.
4. **Later**: Native Shopify/WooCommerce adapters with OAuth install, analytics
   dashboard, human handoff workflows.
