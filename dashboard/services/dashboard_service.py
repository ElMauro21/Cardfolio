from django.db.models import Sum, F
from collection.models import CardTransaction, UserCard
from collection.services.portfolio_service import get_current_portfolio_value
from decimal import Decimal

def get_total_invested(user):
    """
    Returns the total amount of money invested by the user
    through BUY transactions.
    """
    result = (
        CardTransaction.objects
        .filter(
            user=user,
            transaction_type=CardTransaction.BUY,
            price_per_unit__isnull=False,
        )
        .aggregate(
            total=Sum(F("quantity") * F("price_per_unit"))
        )
    )

    return result["total"] or 0

def get_total_earned(user):
    """
    Returns the total amount of money earned by the user
    through SELL transactions.
    """
    result = (
        CardTransaction.objects
        .filter(
            user=user,
            transaction_type=CardTransaction.SELL,
            price_per_unit__isnull=False,
        )
        .aggregate(
            total=Sum(F("quantity") * F("price_per_unit"))
        )
    )

    return result["total"] or 0

def get_unrealized_pl(user):
    """
    Returns the user's unrealized profit or loss (P/L).

    Unrealized P/L is the difference between the current portfolio
    market value and the total amount invested in held cards.
    """
    unrealized_profit_loss = (get_current_portfolio_value(user) or Decimal("0")) - (get_total_invested(user) or Decimal("0"))
    return unrealized_profit_loss

def get_roi_percentage(user): 
    """
    Returns the user's ROI (Return On Investment) percentage.

    ROI is calculated as:
        (Unrealized Profit / Total Invested) * 100

    Returns Decimal("0") if the user has no investments.
    """
    total_invested = get_total_invested(user)

    if not total_invested or total_invested == 0:
        return Decimal("0")
    
    unrealized_pl = get_unrealized_pl(user)

    return (unrealized_pl / total_invested) * Decimal("100")

def get_total_roi_percentage(user):
    """
    Returns the user's total ROI (Return On Investment) percentage.

    Total ROI includes both realized profits (from sold cards)
    and unrealized profits or losses (from current holdings).

    Formula:
        Total ROI % = (Realized P/L + Unrealized P/L) / Total Invested × 100

    Returns Decimal("0") if the user has no investments.
    """
    total_invested = get_total_invested(user)

    if not total_invested or total_invested == 0:
        return Decimal("0")

    total_pl = get_total_earned(user) + get_unrealized_pl(user)

    return (total_pl / total_invested) * Decimal("100")