# 🛍️ E-commerce AI Assistant

An AI-powered customer support assistant that any online store can plug into.
Store owners connect to our API, and their customers get instant, accurate answers
about products and orders — powered by AI with real-time data lookup.

> **Current status:** MVP with **fake sample data** for testing.
> The AI is fully functional — it just needs to be pointed at real store data to go live.

---

## 📖 Table of Contents

- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Quick Start (Run Locally)](#-quick-start-run-locally)
- [Understanding the Fake Test Data](#-understanding-the-fake-test-data)
- [Configure It for YOUR Store](#-configure-it-for-your-store)
- [API Reference](#-api-reference)
- [How the AI Handles Questions](#-how-the-ai-handles-questions)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)

---

## 🧠 How It Works

```
Customer on Store A's website
        │
        │  "Do you have red shirts?"
        ▼
┌──────────────────────────┐
│  Our FastAPI Server      │
│  POST /chat              │
│                          │
│  1. Check API key        │──▶ Which store is this? → store_a
│  2. Send question to AI  │──▶ Groq LLM (tool-calling)
│  3. AI calls tools       │──▶ search_products("red shirt")
│  4. Tools fetch data     │──▶ data/store_a/products.json
│  5. AI writes answer     │
│  6. Return answer        │
└──────────────────────────┘
        │
        ▼
  "Yes! We have a Red Shirt — 20.00 USD, 5 in stock."
```

**Key principle:** The AI **never invents** prices, stock, or order info. It only
reports what the tools actually find in the store's data. If it doesn't know, it
says so and offers to connect the customer to human support.

---

## 📁 Project Structure

```
ecommerce-ai-assistant/
│
├── main.py              # FastAPI server — /chat endpoint
├── keys.py              # API key → store_id mapping
├── data.py              # Loads products.json / orders.json for a store
├── ai_brain.py          # AI agent loop (Groq LLM + tool-calling)
├── tools.py             # Tools the AI can call (search_products, get_order_status)
├── test_ai.py           # Standalone AI test script (no server needed)
├── ui.html              # Chat UI for testing (open in browser)
│
├── data/                # ⬅️ STORE DATA LIVES HERE
│   └── store_a/         #    One folder per store
│       ├── products.json
│       └── orders.json
│
├── .env                 # Your LLM API key (never commit this)
├── .env.example         # Template for .env
├── requirements.txt     # Python dependencies
└── .gitignore
```

---

## ⚙️ Tech Stack

| Component        | Technology                         |
|------------------|------------------------------------|
| Web Server       | **FastAPI** + **Uvicorn**          |
| AI Model         | **Groq** (OpenAI-compatible API)   |
| AI SDK           | **openai** Python package          |
| Data (MVP)       | **JSON files** (fake sample data)  |
| Environment      | **python-dotenv** for secrets      |
| Test UI          | **Vanilla HTML/CSS/JS**            |

---

## 🚀 Quick Start (Run Locally)

### 1. Clone & install

```bash
git clone https://github.com/Abdelmalek-Zouaoui/ecommerce-ai-assistant.git
cd ecommerce-ai-assistant

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Set up your environment

```bash
cp .env.example .env
```

Edit `.env` and add your **Groq API key**:

```env
LLM_API_KEY=gsk_your_groq_api_key_here
```

> 🔑 Get a free API key at [console.groq.com](https://console.groq.com)

### 3. Start the server

```bash
uvicorn main:app --reload
```

The server runs at `http://127.0.0.1:8000`. You can check the auto-generated
API docs at `http://127.0.0.1:8000/docs`.

### 4. Test it

**Option A — Chat UI:** Open `ui.html` in your browser. It connects to the
local server automatically.

**Option B — cURL:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Do you have red shirts?", "api_key": "sk_store_a"}'
```

**Option C — AI-only test (no server needed):**
```bash
python test_ai.py
```

---

## 🧪 Understanding the Fake Test Data

> ⚠️ **The project currently uses fake (sample) data for testing purposes.**
> This data is NOT from a real store. It exists so we can build and test the
> entire AI pipeline without needing a real product catalog or order system.

### What's included

The sample store `store_a` comes with **5 fake products** and **4 fake orders**:

**Products** (`data/store_a/products.json`):

| ID   | Name           | Price  | Stock | Category |
|------|----------------|--------|-------|----------|
| `p1` | Red Shirt      | $20.00 | 5     | shirts   |
| `p2` | Blue Jeans     | $45.00 | 12    | pants    |
| `p3` | Black Sneakers | $60.00 | 0     | shoes    |
| `p4` | Green Hoodie   | $35.00 | 8     | hoodies  |
| `p5` | White Polo     | $25.00 | 3     | shirts   |

**Orders** (`data/store_a/orders.json`):

| ID    | Customer     | Status     | Items                      | Total  |
|-------|-------------|------------|----------------------------|--------|
| `101` | Alice Johnson | shipped    | Red Shirt, Blue Jeans      | $65.00 |
| `102` | Bob Smith     | processing | Green Hoodie               | $35.00 |
| `103` | Carol Davis   | delivered  | Black Sneakers, White Polo | $85.00 |
| `104` | Dave Wilson   | cancelled  | Red Shirt                  | $20.00 |

This fake data lets you test scenarios like:
- ✅ Searching for products that exist (`"Do you have shirts?"`)
- ✅ Searching for products that don't exist (`"Do you have hats?"`)
- ✅ Checking orders with different statuses (shipped, processing, delivered, cancelled)
- ✅ Out-of-stock items (Black Sneakers has `stock: 0`)
- ✅ Invalid order IDs (`"Where is order #999?"`)

---

## 🏪 Configure It for YOUR Store

To connect your own store, you need to do **3 things**: create an API key,
add your data files, and (optionally) update the test UI.

### Step 1 — Create an API key for your store

Open `keys.py` and add your store to the `VALID_KEYS` dictionary:

```python
VALID_KEYS = {
    "sk_store_a": "store_a",       # ← sample store (can remove later)
    "sk_my_store": "my_store",     # ← ADD YOUR STORE HERE
}
```

- **The key** (e.g. `sk_my_store`) is the secret password your website will send
  with every request. Make it hard to guess in production.
- **The value** (e.g. `my_store`) is the internal store ID — it tells the system
  which data folder to load.

### Step 2 — Add your product & order data

Create a new folder under `data/` named exactly like your store ID:

```
data/
├── store_a/          # existing sample store
│   ├── products.json
│   └── orders.json
└── my_store/         # ⬅️ YOUR NEW FOLDER
    ├── products.json
    └── orders.json
```

#### `products.json` format

Your products file must be a JSON array. Each product **must** have at least
`id`, `name`, `price`, and `stock`. The optional fields `description`,
`category`, and `currency` are highly recommended:

```json
[
  {
    "id": "p1",
    "name": "Classic White T-Shirt",
    "description": "100% organic cotton crew neck t-shirt",
    "price": 29.99,
    "currency": "USD",
    "stock": 50,
    "category": "t-shirts"
  },
  {
    "id": "p2",
    "name": "Leather Wallet",
    "description": "Genuine leather bifold wallet with RFID blocking",
    "price": 45.00,
    "currency": "USD",
    "stock": 15,
    "category": "accessories"
  }
]
```

> **Required fields:** `id`, `name`, `price`, `stock`
>
> **Recommended fields:** `description` (helps AI search accuracy),
> `category` (enables category-based queries), `currency` (defaults display;
> always include it so the AI reports the correct currency)

#### `orders.json` format

Your orders file must be a JSON array. Each order **must** have at least
`id` and `status`:

```json
[
  {
    "id": "1001",
    "customer_name": "Jane Doe",
    "status": "shipped",
    "items": ["Classic White T-Shirt"],
    "total": 29.99,
    "currency": "USD",
    "tracking_number": "TRK-ABC123"
  },
  {
    "id": "1002",
    "customer_name": "John Smith",
    "status": "processing",
    "items": ["Leather Wallet"],
    "total": 45.00,
    "currency": "USD",
    "tracking_number": null
  }
]
```

> **Required fields:** `id`, `status`
>
> **Recommended fields:** `customer_name`, `items`, `total`, `currency`,
> `tracking_number`
>
> **Valid statuses:** Use whatever your store uses (e.g. `processing`,
> `shipped`, `delivered`, `cancelled`). The AI will report them as-is.

### Step 3 — Update the test UI (optional)

If you use `ui.html` for testing, open it and add your key to the settings
panel dropdown. Find the `<select id="api-key">` element and add an option:

```html
<select id="api-key">
  <option value="sk_store_a">sk_store_a → store_a</option>
  <option value="sk_my_store">sk_my_store → my_store</option>  <!-- ADD THIS -->
</select>
```

### Step 4 — Test it

Restart the server, then try:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What products do you have?", "api_key": "sk_my_store"}'
```

The AI will now answer using **your** data.

---

## 📡 API Reference

### `POST /chat`

Send a customer question and receive an AI-generated answer.

**Request:**

```json
{
  "question": "Do you have red shirts?",
  "api_key": "sk_store_a"
}
```

| Field      | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `question` | string | ✅       | The customer's question              |
| `api_key`  | string | ✅       | The API key assigned to your store   |

**Response (200):**

```json
{
  "answer": "Yes! We have a Red Shirt — a comfortable cotton t-shirt in bright red, priced at 20.00 USD with 5 in stock."
}
```

**Error responses:**

| Status | Detail                | Cause                        |
|--------|-----------------------|------------------------------|
| 400    | `Missing 'question'`  | No question provided         |
| 400    | `Missing 'api_key'`   | No API key provided          |
| 401    | `Invalid API key`     | Key not found in `keys.py`   |

---

## 🤖 How the AI Handles Questions

The AI uses **tool-calling** — it decides what data it needs and fetches it
through Python functions:

| Tool                | What it does                                       |
|---------------------|----------------------------------------------------|
| `search_products`   | Searches the store's catalog by name, description, or category. Supports fuzzy matching (e.g. "hoody" finds "Hoodie"). |
| `get_order_status`  | Looks up a specific order by its ID and returns full details (status, items, tracking number). |

### Safety & quality rules built into the AI:

- ✅ **Never invents data** — only reports what tools return
- ✅ **Stays on topic** — declines off-topic requests (jokes, coding help, etc.)
- ✅ **Handles sensitive data** — if a customer shares a credit card or SSN, the AI tells them it's not needed and doesn't repeat it
- ✅ **Prompt injection resistant** — treats tool data as data only, not instructions
- ✅ **Respects currency** — always uses the currency from the data, never assumes or converts
- ✅ **Graceful failures** — if data is missing or malformed, offers to connect to human support

---

## 🧪 Testing

### Run the standalone AI test

```bash
python test_ai.py
```

This tests the AI brain directly (no server needed) with 5 sample questions
covering product search, order lookup, out-of-stock, and pricing queries.

### Test via the server

```bash
# Start the server
uvicorn main:app --reload

# Product search
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Do you have any shoes?", "api_key": "sk_store_a"}'

# Order status
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is order 101?", "api_key": "sk_store_a"}'

# Invalid key (should return 401)
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello", "api_key": "invalid_key"}'
```

### Test via the Chat UI

Open `ui.html` in any browser. Select your API key from the settings panel
(⚙️ icon), and start chatting.

---

## 🚢 Deployment

To deploy the server so real stores can connect:

1. **Host on** [Render](https://render.com), [Railway](https://railway.app), or
   [Fly.io](https://fly.io)
2. **Set the environment variable** `LLM_API_KEY` as a host secret (never commit it)
3. **Upload your store data** (`data/<store_id>/`) alongside the code
4. **Share the public URL** and API key with each store owner

Their website integration is a single `fetch` call:

```javascript
const response = await fetch("https://your-server.com/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    question: customerMessage,
    api_key: "sk_their_store"
  })
});
const { answer } = await response.json();
```

---

## 🗺️ Roadmap

| Phase | Feature                        | Status       |
|-------|--------------------------------|--------------|
| MVP   | AI assistant with fake data    | ✅ Done       |
| MVP   | FastAPI server + API keys      | ✅ Done       |
| MVP   | Chat test UI                   | ✅ Done       |
| Next  | Multi-store isolation test     | 🔲 Planned   |
| Next  | Error handling & rate limiting  | 🔲 Planned   |
| Later | Real store data connectors     | 🔲 Planned   |
| Later | Shopify / WooCommerce plugins  | 🔲 Planned   |
| Later | Store owner signup dashboard   | 🔲 Planned   |
| Later | Usage billing & limits         | 🔲 Planned   |

---

## 👥 Team

| Person    | Responsibility                                      |
|-----------|-----------------------------------------------------|
| **Amine** | Server, API keys, data loading, deployment, UI      |
| **Malek** | AI brain, tools, prompt engineering, answer quality  |

---

## 📝 License

This project is for educational / demonstration purposes.
