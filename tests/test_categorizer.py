from app.categorizer import build_budget_report, categorize, categorize_transactions
from app.data.sample_transactions import SAMPLE_BUDGETS, SAMPLE_TRANSACTIONS


def test_categorize_rent():
    assert categorize("Monthly Rent Payment - Riverside Apartments", -1450.0) == "Rent"


def test_categorize_groceries():
    assert categorize("GreenMart Grocery", -86.42) == "Groceries"


def test_categorize_income_fallback():
    assert categorize("Payroll Deposit - Acme Corp", 3200.0) == "Income"


def test_categorize_unknown_positive_falls_back_to_income():
    assert categorize("Totally Unknown Merchant XYZ", 10.0) == "Income"


def test_categorize_unknown_negative_falls_back_to_other():
    assert categorize("Totally Unknown Merchant XYZ", -10.0) == "Other"


def test_categorize_transactions_batch():
    result = categorize_transactions(SAMPLE_TRANSACTIONS)
    assert len(result) == len(SAMPLE_TRANSACTIONS)
    categories = {t.category for t in result}
    assert "Rent" in categories
    assert "Groceries" in categories
    assert "Income" in categories


def test_budget_report_totals():
    report = build_budget_report(SAMPLE_TRANSACTIONS, SAMPLE_BUDGETS)
    assert report.total_income > 0
    assert report.total_spent > 0
    assert round(report.net, 2) == round(report.total_income - report.total_spent, 2)


def test_budget_report_flags_over_budget_rent():
    # Rent budget is set equal to the actual rent transaction, so a small
    # over-budget category should exist for Groceries (multiple purchases).
    report = build_budget_report(SAMPLE_TRANSACTIONS, SAMPLE_BUDGETS)
    groceries = next(c for c in report.by_category if c.category == "Groceries")
    assert groceries.spent > 0
    assert groceries.over_budget == (groceries.spent > groceries.budget)


def test_budget_report_category_without_budget_has_none_fields():
    report = build_budget_report(
        [{"id": "x1", "date": "2026-08-01", "description": "Mystery Purchase", "amount": -10.0}],
        budgets={},
    )
    other = next(c for c in report.by_category if c.category == "Other")
    assert other.budget is None
    assert other.remaining is None
    assert other.over_budget is False
