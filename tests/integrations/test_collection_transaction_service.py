import pytest
from collection.services.transaction_service import apply_card_transaction
from collection.models import UserCard, CardTransaction


@pytest.mark.integration
def test_buy_creates_usercard_and_transaction(db, user, card):
    user_card = apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=2,
        price_per_unit=10,
    )

    assert user_card is not None
    assert user_card.quantity == 2

    tx = CardTransaction.objects.get()
    assert tx.transaction_type == CardTransaction.BUY
    assert tx.quantity == 2
    assert tx.price_per_unit == 10


@pytest.mark.integration
def test_buy_increments_existing_usercard(db, user, card):
    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
    )

    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=3,
    )

    user_card = UserCard.objects.get(user=user, card=card)
    assert user_card.quantity == 4
    assert CardTransaction.objects.count() == 2


@pytest.mark.integration
def test_sell_decreases_quantity(db, user, card):
    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=3,
    )

    user_card = apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.SELL,
        quantity=2,
        price_per_unit=50,
    )

    assert user_card.quantity == 1
    assert CardTransaction.objects.count() == 2


@pytest.mark.integration
def test_sell_last_card_deletes_usercard(db, user, card):
    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
    )

    user_card = apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.SELL,
        quantity=1,
        price_per_unit=100,
    )

    assert user_card is None
    assert not UserCard.objects.filter(user=user, card=card).exists()
    assert CardTransaction.objects.count() == 2


@pytest.mark.integration
def test_sell_fails_if_not_enough_cards(db, user, card):
    apply_card_transaction(
        user=user,
        card=card,
        transaction_type=CardTransaction.BUY,
        quantity=1,
    )

    with pytest.raises(ValueError, match="Not enough cards"):
        apply_card_transaction(
            user=user,
            card=card,
            transaction_type=CardTransaction.SELL,
            quantity=2,
        )

    user_card = UserCard.objects.get(user=user, card=card)
    assert user_card.quantity == 1
    assert CardTransaction.objects.count() == 1


@pytest.mark.integration
def test_transaction_rejects_zero_quantity(db, user, card):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        apply_card_transaction(
            user=user,
            card=card,
            transaction_type=CardTransaction.BUY,
            quantity=0,
        )

    assert UserCard.objects.count() == 0
    assert CardTransaction.objects.count() == 0


@pytest.mark.integration
def test_transaction_rejects_invalid_type(db, user, card):
    with pytest.raises(ValueError, match="Invalid transaction type"):
        apply_card_transaction(
            user=user,
            card=card,
            transaction_type="invalid",
            quantity=1,
        )

    assert UserCard.objects.count() == 0
    assert CardTransaction.objects.count() == 0
