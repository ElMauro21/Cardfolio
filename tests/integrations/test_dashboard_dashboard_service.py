import pytest

from dashboard.services.dashboard_service import (
    get_total_invested,
    get_total_earned,
    get_roi_percentage,
    get_total_roi_percentage)
from collection.services.transaction_service import apply_card_transaction
from collection.models import CardTransaction
from decimal import Decimal

@pytest.mark.integration
def test_get_total_invested_return_zero_when_no_buys(db,user):
    total = get_total_invested(user)
    assert total == 0

@pytest.mark.integration
def test_get_total_invested_sums_buy_transaction(db, user, card):
    CardTransaction.objects.create(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=2,
        price_per_unit=10
    )

    CardTransaction.objects.create(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
        price_per_unit=5,
    )

    total = get_total_invested(user)
    assert total == 25

@pytest.mark.integration
def test_get_total_earned_return_zero_when_no_buys(db,user):
    total = get_total_earned(user)
    assert total == 0

@pytest.mark.integration
def test_get_total_earned_sums_sell_transaction(db, user, card):
    CardTransaction.objects.create(
        user=user,
        card=card,
        transaction_type=CardTransaction.SELL,
        quantity=2,
        price_per_unit=10
    )

    total = get_total_earned(user)
    assert total == 20

@pytest.mark.integration
def test_get_roi_percentege(db, user, card):
    card.price_usd = Decimal("150")
    card.save()

    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
        price_per_unit=Decimal("100"),
    )

    roi = get_roi_percentage(user)
    assert roi == Decimal("50")

@pytest.mark.integration
def test_get_total_roi_percentage(db, user, card):

    card.price_usd = Decimal("150")
    card.save()

    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
        price_per_unit=Decimal("100"),
    )

    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.SELL,
        quantity=1,
        price_per_unit=Decimal("120"),
    )

    roi = get_total_roi_percentage(user)

    assert roi == Decimal("20")