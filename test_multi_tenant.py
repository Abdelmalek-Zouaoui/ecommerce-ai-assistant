"""
test_multi_tenant.py — end-to-end multi-tenant isolation test
Owner: AMINE + MALEK

Run with:  python test_multi_tenant.py
Hits the real /chat endpoint (via FastAPI's TestClient) for both stores and
confirms store_a and store_b never see each other's products or orders —
even for order id "101", which exists in both stores with different data.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

checks = []


def check(label, condition):
    checks.append((label, condition))
    print(f"{'PASS' if condition else 'FAIL'}: {label}")


def chat(question, api_key):
    response = client.post("/chat", json={"question": question, "api_key": api_key})
    return response


# --- Auth edge cases ---
r = chat("hello", "sk_not_a_real_key")
check("unknown api_key -> 401", r.status_code == 401)

r = client.post("/chat", json={"api_key": "sk_store_a"})
check("missing question -> 400", r.status_code == 400)

r = client.post("/chat", json={"question": "hello"})
check("missing api_key -> 400", r.status_code == 400)

# --- Product isolation ---
r = chat("What products do you sell? List their names.", "sk_store_a")
answer_a = r.json()["answer"]
print(f"\nstore_a products answer: {answer_a}\n")
check("store_a sees its own product (Red Shirt)", "red shirt" in answer_a.lower())
check("store_a does NOT see store_b's product (Leather Wallet)", "leather wallet" not in answer_a.lower())

r = chat("What products do you sell? List their names.", "sk_store_b")
answer_b = r.json()["answer"]
print(f"\nstore_b products answer: {answer_b}\n")
check("store_b sees its own product (Leather Wallet)", "leather wallet" in answer_b.lower())
check("store_b does NOT see store_a's product (Red Shirt)", "red shirt" not in answer_b.lower())

# --- Order isolation (same order id "101" exists in both stores, different data) ---
r = chat("What's the status of order 101?", "sk_store_a")
order_a = r.json()["answer"]
print(f"\nstore_a order 101 answer: {order_a}\n")
check("store_a order 101 shows its own status (shipped)", "shipped" in order_a.lower())
check("store_a order 101 does NOT leak store_b's customer (Elena Rossi)", "elena rossi" not in order_a.lower())

r = chat("What's the status of order 101?", "sk_store_b")
order_b = r.json()["answer"]
print(f"\nstore_b order 101 answer: {order_b}\n")
check("store_b order 101 shows its own status (processing)", "processing" in order_b.lower())
check("store_b order 101 does NOT leak store_a's customer (Alice Johnson)", "alice johnson" not in order_b.lower())

failed = [label for label, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
if failed:
    print("FAILED:", ", ".join(failed))
