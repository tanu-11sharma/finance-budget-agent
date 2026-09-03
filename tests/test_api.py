from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["sample_transaction_count"] > 0


def test_transactions_listed():
    resp = client.get("/transactions")
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_summary_default():
    resp = client.get("/summary")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_income"] > 0
    assert body["total_spent"] > 0
    assert any(c["category"] == "Groceries" for c in body["by_category"])


def test_categorize_endpoint():
    resp = client.post(
        "/categorize",
        json={
            "transactions": [
                {"id": "z1", "date": "2026-08-01", "description": "GreenMart Grocery", "amount": -20.0}
            ]
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["category"] == "Groceries"


def test_summary_custom_budget():
    resp = client.post(
        "/summary",
        json={
            "transactions": [
                {"id": "z2", "date": "2026-08-01", "description": "GreenMart Grocery", "amount": -500.0}
            ],
            "budgets": {"Groceries": 100.0},
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    groceries = next(c for c in body["by_category"] if c["category"] == "Groceries")
    assert groceries["over_budget"] is True
