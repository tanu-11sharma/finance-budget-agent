"""
FastAPI app exposing the Finance Budget Agent demo.

DEMO / NON-PRODUCTION NOTICE: this app categorizes and summarizes sample,
synthetic transaction data using simple rules. It does NOT connect to any
real bank or account, does not move money, and is not financial advice.

Endpoints:
  GET  /health         -> liveness check
  GET  /transactions    -> raw sample transactions
  POST /categorize       -> categorize a custom list of transactions
  GET  /summary           -> monthly category summary vs. sample budget for
                             the bundled sample transactions
  POST /summary            -> same, but for a custom list of transactions
                             and/or custom budget

Run locally:
  uvicorn app.main:app --reload

Example usage:
  curl -s http://127.0.0.1:8000/summary
"""

from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.categorizer import build_budget_report, categorize_transactions
from app.data.sample_transactions import SAMPLE_BUDGETS, SAMPLE_TRANSACTIONS

app = FastAPI(
    title="Finance Budget Agent (Demo)",
    description=(
        "Rule-based personal transaction categorizer and budget-vs-actual "
        "summary over synthetic sample data. Demo only - not connected to "
        "any real bank or account, and not financial advice."
    ),
    version="0.1.0",
)


class Transaction(BaseModel):
    id: str
    date: str
    description: str
    amount: float


class CategorizeRequest(BaseModel):
    transactions: List[Transaction]


class CategorizedTransactionOut(BaseModel):
    id: str
    date: str
    description: str
    amount: float
    category: str


class CategorySummaryOut(BaseModel):
    category: str
    spent: float
    budget: Optional[float]
    remaining: Optional[float]
    over_budget: bool


class BudgetReportOut(BaseModel):
    transactions: List[CategorizedTransactionOut]
    by_category: List[CategorySummaryOut]
    total_spent: float
    total_income: float
    net: float


class SummaryRequest(BaseModel):
    transactions: Optional[List[Transaction]] = None
    budgets: Optional[Dict[str, float]] = None


def _report_to_out(report) -> BudgetReportOut:
    return BudgetReportOut(
        transactions=[
            CategorizedTransactionOut(
                id=t.id, date=t.date, description=t.description, amount=t.amount, category=t.category
            )
            for t in report.transactions
        ],
        by_category=[
            CategorySummaryOut(
                category=c.category, spent=c.spent, budget=c.budget, remaining=c.remaining, over_budget=c.over_budget
            )
            for c in report.by_category
        ],
        total_spent=report.total_spent,
        total_income=report.total_income,
        net=report.net,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "sample_transaction_count": len(SAMPLE_TRANSACTIONS)}


@app.get("/transactions")
def get_transactions() -> List[dict]:
    return SAMPLE_TRANSACTIONS


@app.post("/categorize", response_model=List[CategorizedTransactionOut])
def categorize(req: CategorizeRequest) -> List[CategorizedTransactionOut]:
    txns = [t.model_dump() for t in req.transactions]
    categorized = categorize_transactions(txns)
    return [
        CategorizedTransactionOut(
            id=t.id, date=t.date, description=t.description, amount=t.amount, category=t.category
        )
        for t in categorized
    ]


@app.get("/summary", response_model=BudgetReportOut)
def summary_default() -> BudgetReportOut:
    report = build_budget_report(SAMPLE_TRANSACTIONS, SAMPLE_BUDGETS)
    return _report_to_out(report)


@app.post("/summary", response_model=BudgetReportOut)
def summary_custom(req: SummaryRequest) -> BudgetReportOut:
    txns = [t.model_dump() for t in req.transactions] if req.transactions else SAMPLE_TRANSACTIONS
    budgets = req.budgets if req.budgets is not None else SAMPLE_BUDGETS
    report = build_budget_report(txns, budgets)
    return _report_to_out(report)
