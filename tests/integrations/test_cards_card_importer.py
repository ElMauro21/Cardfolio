import pytest 

from cards.models import Card
from cards.services.card_importer import import_exact_mtg_card

@pytest.mark.integration
def test_import_creates_card_when_not_exists(db, mocker,fake_scryfall_card_data):
    fake_data = fake_scryfall_card_data()
    mocker.patch(
        "cards.services.card_importer.fetch_card",
        return_value = fake_data
    )

    card = import_exact_mtg_card(
        set_code="lea",
        collector_number="233",
        is_foil=True,
    )

    assert card.id is not None
    assert card.name == fake_data["name"]
    assert card.finish == "foil"
    assert Card.objects.count() == 1

@pytest.mark.integration
def test_import_is_idempotent(db,mocker,fake_scryfall_card_data):
    mocker.patch(
        "cards.services.card_importer.fetch_card",
        return_value = fake_scryfall_card_data()
    )

    card_1 = import_exact_mtg_card(
        set_code = "lea",
        collector_number = "233",
        is_foil = True,
    )

    card_2 = import_exact_mtg_card(
        set_code = "lea",
        collector_number = "233",
        is_foil = True,
    )

    assert card_1.id == card_2.id
    assert Card.objects.count() ==1

@pytest.mark.integration
def test_import_raises_error_when_card_not_found(db,mocker):
    mocker.patch(
        "cards.services.card_importer.fetch_card",
        return_value = None
    )

    with pytest.raises(ValueError, match="Card not found"):
        import_exact_mtg_card(
            set_code = "lea",
            collector_number = "999",
            is_foil = True,
        )

@pytest.mark.integration
def test_import_raises_error_when_foil_not_available(db, mocker,fake_scryfall_card_data):
    fake_data = fake_scryfall_card_data(
        finishes=["nonfoil"]
    )

    mocker.patch(
        "cards.services.card_importer.fetch_card",
        return_value = fake_data
    )

    with pytest.raises(ValueError, match="foil version"):
        import_exact_mtg_card(
            set_code="lea",
            collector_number="1",
            is_foil=True,
        )

@pytest.mark.integration
def test_import_raises_error_when_nonfoil_not_available(db, mocker,fake_scryfall_card_data):
    fake_data = fake_scryfall_card_data(
        finishes=["foil"]
    )

    mocker.patch(
        "cards.services.card_importer.fetch_card",
        return_value=fake_data
    )

    with pytest.raises(ValueError, match="non-foil"):
        import_exact_mtg_card(
            set_code="lea",
            collector_number="233",
            is_foil=False, 
        )