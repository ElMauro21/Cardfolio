import pytest

from collection.services.collection_service import add_card_to_collection
from collection.models import UserCard

@pytest.mark.integration
def test_add_card_creates_usercard(db,user,card):
    user_card = add_card_to_collection(
        user = user,
        card = card,
        quantity = 2,
        purchase_price = 10
    )

    assert user_card.quantity == 2
    assert UserCard.objects.count() == 1

@pytest.mark.integration
def test_add_card_increments_quantity(db, user, card):
    add_card_to_collection(user=user, card=card, quantity=1)
    user_card = add_card_to_collection(user=user, card=card, quantity=2)

    assert user_card.quantity == 3
    assert UserCard.objects.count() == 1

@pytest.mark.integration
def test_add_card_updates_purchase_price_when_provided(db, user, card):
    add_card_to_collection(user=user, card=card, quantity=1, purchase_price=5)
    user_card = add_card_to_collection(
        user=user, card=card, quantity=1, purchase_price=8
    )

    assert user_card.purchase_price == 8

@pytest.mark.unit
def test_add_card_rejects_invalid_quantity(user, card):
    with pytest.raises(ValueError):
        add_card_to_collection(
            user=user,
            card=card,
            quantity=0
        )

