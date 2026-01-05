import pytest
from django.db import IntegrityError
from cards.models import Card

@pytest.mark.integration
def test_card_unique_constraint_on_scryfall_id_and_finish(db):
    Card.objects.create(
        name = "Black Lotus",
        scryfall_id = "abc123",
        finish="foil",
        set_code="lea",
        set_name="Limited Edition Alpha",
        rarity="rare",
        collector_number="233", 
    )

    with pytest.raises(IntegrityError):
        Card.objects.create(
            name="Black Lotus",
            scryfall_id="abc123",
            finish="foil",
            set_code="lea",
            set_name="Limited Edition Alpha",
            rarity="rare",
            collector_number="233",
        )