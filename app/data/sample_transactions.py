"""
Synthetic sample transaction data for the Finance Budget Agent demo.

All transactions below are entirely fabricated for demonstration purposes.
They do not represent any real person's bank account, spending, or income.
This project is a categorization/budgeting DEMO, not a real financial tool,
and does not connect to any bank, card network, or live account.
"""

SAMPLE_TRANSACTIONS = [
    {"id": "t001", "date": "2026-08-01", "description": "Monthly Rent Payment - Riverside Apartments", "amount": -1450.00},
    {"id": "t002", "date": "2026-08-02", "description": "GreenMart Grocery", "amount": -86.42},
    {"id": "t003", "date": "2026-08-02", "description": "Payroll Deposit - Acme Corp", "amount": 3200.00},
    {"id": "t004", "date": "2026-08-03", "description": "Metro Transit Card Reload", "amount": -40.00},
    {"id": "t005", "date": "2026-08-04", "description": "Sunrise Coffee House", "amount": -5.75},
    {"id": "t006", "date": "2026-08-05", "description": "CityPower Electric Bill", "amount": -112.30},
    {"id": "t007", "date": "2026-08-06", "description": "Streamflix Subscription", "amount": -15.99},
    {"id": "t008", "date": "2026-08-07", "description": "GreenMart Grocery", "amount": -63.10},
    {"id": "t009", "date": "2026-08-08", "description": "Blue Bicycle Bike Repair", "amount": -35.00},
    {"id": "t010", "date": "2026-08-09", "description": "Trattoria Bella Dinner", "amount": -58.20},
    {"id": "t011", "date": "2026-08-10", "description": "Pharmacy Plus - Prescription", "amount": -24.60},
    {"id": "t012", "date": "2026-08-11", "description": "Cinema City Movie Tickets", "amount": -28.00},
    {"id": "t013", "date": "2026-08-12", "description": "WaterWorks Utility Bill", "amount": -45.10},
    {"id": "t014", "date": "2026-08-13", "description": "GreenMart Grocery", "amount": -71.95},
    {"id": "t015", "date": "2026-08-14", "description": "Rideshare Trip - QuickCab", "amount": -18.40},
    {"id": "t016", "date": "2026-08-15", "description": "ClothCo Online Order", "amount": -92.50},
    {"id": "t017", "date": "2026-08-16", "description": "Payroll Deposit - Acme Corp", "amount": 3200.00},
    {"id": "t018", "date": "2026-08-16", "description": "Gym Membership - FitZone", "amount": -40.00},
    {"id": "t019", "date": "2026-08-17", "description": "Sunrise Coffee House", "amount": -6.25},
    {"id": "t020", "date": "2026-08-18", "description": "Internet Bill - FiberLink", "amount": -59.99},
    {"id": "t021", "date": "2026-08-19", "description": "GreenMart Grocery", "amount": -77.35},
    {"id": "t022", "date": "2026-08-20", "description": "Trattoria Bella Dinner", "amount": -64.10},
    {"id": "t023", "date": "2026-08-21", "description": "Rideshare Trip - QuickCab", "amount": -22.15},
    {"id": "t024", "date": "2026-08-22", "description": "Streamflix Subscription", "amount": -15.99},
    {"id": "t025", "date": "2026-08-23", "description": "MusicWave Subscription", "amount": -9.99},
    {"id": "t026", "date": "2026-08-24", "description": "Pharmacy Plus - Vitamins", "amount": -18.30},
    {"id": "t027", "date": "2026-08-25", "description": "GreenMart Grocery", "amount": -68.05},
    {"id": "t028", "date": "2026-08-26", "description": "Metro Transit Card Reload", "amount": -40.00},
    {"id": "t029", "date": "2026-08-27", "description": "Freelance Design Payment - Studio Nine", "amount": 450.00},
    {"id": "t030", "date": "2026-08-28", "description": "ClothCo Online Order", "amount": -47.20},
]

# A simple monthly budget by category, used to flag over/under spending.
# Entirely illustrative sample numbers.
SAMPLE_BUDGETS = {
    "Rent": 1450.00,
    "Groceries": 300.00,
    "Dining": 120.00,
    "Transport": 100.00,
    "Utilities": 220.00,
    "Subscriptions": 40.00,
    "Entertainment": 40.00,
    "Health": 50.00,
    "Shopping": 100.00,
    "Fitness": 40.00,
    "Income": 0.00,
    "Other": 0.00,
}
