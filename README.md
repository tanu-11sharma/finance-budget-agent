# Finance Budget Agent (Demo)

A rule-based personal-finance agent that categorizes transactions and
compares actual spend against a monthly budget, category by category -
built on entirely synthetic sample data.

**This is a demo/reference project, not a real financial tool.** It does
not connect to any bank, card network, or live account; it does not move
money; and nothing it outputs is financial advice.

## What it does

1. Takes a list of transactions (`{id, date, description, amount}`).
2. Categorizes each one with transparent keyword rules (`app/categorizer.py`)
   into categories like Rent, Groceries, Dining, Transport, Utilities,
   Subscriptions, and Income.
3. Rolls categorized spend up against a sample monthly budget per category,
   flagging which categories are over budget and by how much.

Every category assignment traces back to a specific keyword rule - there's
no black-box model and no external API call involved in the core logic.

## Why this is relevant

"Agent reads your transactions, tells you where your money went, and flags
what's off-budget" is a common applied-AI pattern in personal-finance
tooling. This project builds a small, fully-working, and fully-inspectable
version of that pattern: rule-based categorization plus a budget-vs-actual
report, exposed as a FastAPI service.

## Project structure

```
app/
  main.py                    FastAPI app (health, transactions, categorize, summary)
  categorizer.py              Keyword-rule categorizer + budget report builder
  data/sample_transactions.py Synthetic sample transactions and sample budget
tests/
  test_categorizer.py         Unit tests for categorization and budget logic
  test_api.py                  Integration tests for the FastAPI endpoints
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API available at `http://127.0.0.1:8000`, interactive docs at
`http://127.0.0.1:8000/docs`.

## Test

```bash
pytest -q
```

All 14 tests run offline against the in-memory sample data and the
FastAPI `TestClient` - no network access required.

## Example usage

Get the monthly budget-vs-actual summary for the bundled sample transactions:

```bash
curl -s http://127.0.0.1:8000/summary
```

Example (real, verified) output - total income/spend for the bundled sample
month, with the first few categories:

```json
{
  "total_income": 6850.0,
  "total_spent": 2616.68,
  "net": 4233.32,
  "by_category": [
    {"category": "Rent", "spent": 1450.0, "budget": 1450.0, "remaining": 0.0, "over_budget": false},
    {"category": "Groceries", "spent": 366.87, "budget": 300.0, "remaining": -66.87, "over_budget": true},
    {"category": "Utilities", "spent": 217.39, "budget": 220.0, "remaining": 2.61, "over_budget": false},
    {"category": "Transport", "spent": 155.55, "budget": 100.0, "remaining": -55.55, "over_budget": true}
  ]
}
```

Categorize your own list of transactions:

```bash
curl -s http://127.0.0.1:8000/categorize \
  -H "Content-Type: application/json" \
  -d '{"transactions": [{"id": "z1", "date": "2026-08-01", "description": "GreenMart Grocery", "amount": -20.0}]}'
```

Run a summary against a custom transaction list and/or custom budget:

```bash
curl -s -X POST http://127.0.0.1:8000/summary \
  -H "Content-Type: application/json" \
  -d '{"budgets": {"Groceries": 100.0}}'
```

## Disclaimer

All transaction and budget data in this repository is synthetic and
fabricated for demonstration purposes - it does not represent any real
person's finances. This project is a non-production demo, not a bank
integration, and not financial advice.

## License

MIT
