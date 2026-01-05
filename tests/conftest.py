import pytest

from django.contrib.auth import get_user_model
from cards.models import Card


@pytest.fixture
def fake_scryfall_card_data():
    """
    Returns minimal valid Scryfall-like card data
    for testing import_exact_mtg_card.

    Tests can override specific fields using dict updates.
    """
    def _factory(**overrides):
        data = {
            "id": "abc123",
            "name": "Test Card",
            "set": "lea",
            "set_name": "Limited Edition Alpha",
            "collector_number": "233",
            "rarity": "rare",
            "finishes": ["foil", "nonfoil"],
            "prices": {
                "usd": "10.00",
                "usd_foil": "12.00",
            },
            "image_uris": {
                "normal": "https://example.com/card.jpg"
            },
        }
        data.update(overrides)
        return data

    return _factory

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="password123"
    )


@pytest.fixture
def card(db):
    return Card.objects.create(
        name="Test Card",
        scryfall_id="abc123",
        finish="nonfoil",
        set_code="lea",
        set_name="Limited Edition Alpha",
        rarity="rare",
        collector_number="233",
        price_usd=10,
        image_url="https://example.com/card.jpg",
    )