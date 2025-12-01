# Purpose: Helpers for labeling nodes and inferring categories.
from typing import Dict

def build_label(base: str, suffix: str = None, address: str = None) -> str:
    """Build a node label with optional account suffix and address."""
    label = base
    if suffix:
        label += f"\nAcct ****{suffix}"
    if address:
        label += f"\n{address}"
    return label

def infer_category(txn: Dict) -> str:
    """Guess transaction category if not explicitly set. Unknowns show as 'combined' (white/no color)."""
    if txn.get("category"):
        return txn["category"]
    memo = (txn.get("memo") or "").lower()
    if "payroll" in memo or "salary" in memo:
        return "employment_income"
    if "loan" in memo or "lender" in memo:
        return "loan"
    if "gift" in memo:
        return "gift"
    return "combined"  # neutral