"""
Rule-based transaction categorizer + budget comparison for the Finance
Budget Agent demo.

DEMO / NON-PRODUCTION NOTICE
-----------------------------
This module is a teaching/demo implementation. It categorizes and
summarizes *sample, synthetic* transaction data using simple keyword
rules. It does not connect to any real bank, card network, or account,
does not move money, and is NOT financial advice. Any resemblance of the
sample data to a real account is coincidental.

How it works
------------
Each transaction description is matched (case-insensitively) against a
small set of keyword -> category rules. The first matching rule wins;
transactions that match nothing fall back to "Other" (or "Income" for
positive amounts with no other match). Category totals are then compared
against a sample monthly budget to flag over/under-budget categories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Ordered keyword -> category rules. Order matters: first match wins.
CATEGORY_RULES: List[tuple[str, List[str]]] = [
    ("Rent", ["rent", "apartments", "landlord"]),
    ("Groceries", ["grocery", "greenmart", "supermarket"]),
    ("Dining", ["trattoria", "restaurant", "dinner", "coffee", "cafe"]),
    ("Transport", ["transit", "rideshare", "quickcab", "bike repair", "fuel", "gas station"]),
    ("Utilities", ["electric", "water", "utility", "internet", "fiberlink", "power"]),
    ("Subscriptions", ["streamflix", "musicwave", "subscription"]),
    ("Entertainment", ["cinema", "movie", "concert", "theater"]),
    ("Health", ["pharmacy", "clinic", "doctor", "prescription", "vitamins"]),
    ("Fitness", ["gym", "fitzone", "fitness"]),
    ("Shopping", ["clothco", "online order", "store", "mall"]),
    ("Income", ["payroll", "deposit", "freelance", "salary", "payment received"]),
]


def categorize(description: str, amount: float) -> str:
    """Return the best-matching category for a transaction."""
    text = description.lower()
    for category, keywords in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return category
    return "Income" if amount > 0 else "Other"


@dataclass
class CategorizedTransaction:
    id: str
    date: str
    description: str
    amount: float
    category: str


@dataclass
class CategorySummary:
    category: str
    spent: float
    budget: Optional[float]
    remaining: Optional[float]
    over_budget: bool


@dataclass
class BudgetReport:
    transactions: List[CategorizedTransaction] = field(default_factory=list)
    by_category: List[CategorySummary] = field(default_factory=list)
    total_spent: float = 0.0
    total_income: float = 0.0
    net: float = 0.0


def categorize_transactions(transactions: List[dict]) -> List[CategorizedTransaction]:
    result = []
    for t in transactions:
        cat = categorize(t["description"], t["amount"])
        result.append(
            CategorizedTransaction(
                id=t["id"],
                date=t["date"],
                description=t["description"],
                amount=t["amount"],
                category=cat,
            )
        )
    return result


def build_budget_report(
    transactions: List[dict], budgets: Dict[str, float]
) -> BudgetReport:
    categorized = categorize_transactions(transactions)

    spend_by_category: Dict[str, float] = {}
    total_income = 0.0
    total_spent = 0.0

    for t in categorized:
        if t.amount >= 0:
            total_income += t.amount
            continue
        spend = -t.amount
        total_spent += spend
        spend_by_category[t.category] = spend_by_category.get(t.category, 0.0) + spend

    summaries: List[CategorySummary] = []
    for category, spent in sorted(spend_by_category.items(), key=lambda kv: -kv[1]):
        budget = budgets.get(category)
        if budget is None:
            summaries.append(
                CategorySummary(category=category, spent=round(spent, 2), budget=None, remaining=None, over_budget=False)
            )
        else:
            remaining = round(budget - spent, 2)
            summaries.append(
                CategorySummary(
                    category=category,
                    spent=round(spent, 2),
                    budget=budget,
                    remaining=remaining,
                    over_budget=spent > budget,
                )
            )

    return BudgetReport(
        transactions=categorized,
        by_category=summaries,
        total_spent=round(total_spent, 2),
        total_income=round(total_income, 2),
        net=round(total_income - total_spent, 2),
    )
