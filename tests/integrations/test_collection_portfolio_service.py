import pytest

from collection.services.portfolio_service import get_current_portfolio_value
from decimal import Decimal
from collection.models import UserCard

@pytest.mark.integration
def test_get_current_portfolio_value_returns_zero_when_no_cards(db,user):
    total_portfolio_value = get_current_portfolio_value(user)

    assert total_portfolio_value == 0

@pytest.mark.integration
def test_get_current_portfolio_value_sums_quantity_times_price(db, user, card):
    card.price_usd = Decimal("10.00")
    card.save()

    UserCard.objects.create(
        user=user,
        card=card,
        quantity=3
    )

    total = get_current_portfolio_value(user)
    assert total == Decimal("30.00")

@pytest.mark.integration
def test_get_current_portfolio_value_ignores_cards_without_price(db, user, card):
    card.price_usd = None
    card.save()

    UserCard.objects.create(
        user=user,
        card=card,
        quantity=5,
    )

    total = get_current_portfolio_value(user)
    assert total == 0