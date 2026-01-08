from collection.models import UserCard
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

def get_current_portfolio_value(user):
    """
    Returns the current market value of the user's portfolio.

    Calculated as:
        SUM(quantity * card.price_usd)

    Only includes cards with a known market price.
    """
    result = (
        UserCard.objects
        .filter(
            user=user,
            card__price_usd__isnull=False,
        )
        .annotate(
            subtotal = ExpressionWrapper(
                F("quantity") * F("card__price_usd"),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
        .aggregate(
            total=Sum("subtotal")
        )
    )

    return result["total"] or 0