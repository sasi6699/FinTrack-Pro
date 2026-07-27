"""Transaction categories shared by all FinTrack Pro pages."""

INCOME_CATEGORIES = (
    "Salary",
    "Bonus",
    "Freelance",
    "Business Income",
    "Investment",
    "Interest",
    "Rental Income",
    "Gift",
    "Refund",
    "Other Income",
)

EXPENSE_CATEGORIES = (
    "Food & Dining",
    "Groceries",
    "Transportation",
    "Fuel",
    "Shopping",
    "Entertainment",
    "Utilities",
    "Internet",
    "Mobile Bill",
    "Rent",
    "Insurance",
    "Healthcare",
    "Education",
    "Travel",
    "Clothing",
    "Personal Care",
    "Fitness",
    "Gifts & Donations",
    "Savings",
    "Loan Payment",
    "Emergency",
    "Miscellaneous",
)

ALL_CATEGORIES = INCOME_CATEGORIES + EXPENSE_CATEGORIES


def categories_for(transaction_type, legacy_category=None):
    """Return the appropriate choices, retaining an edited legacy value safely."""
    categories = list(INCOME_CATEGORIES if transaction_type == "Income" else EXPENSE_CATEGORIES)
    if legacy_category and legacy_category not in categories:
        categories.append(legacy_category)
    return categories
