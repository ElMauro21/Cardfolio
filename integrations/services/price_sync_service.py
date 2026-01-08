from decimal import Decimal
from django.db import transaction

from cards.models import Card
from integrations.services.bulk_reader import iter_bulk_cards 

def sync_card_prices_from_bulk(bulk_file_path):
    """
    Syncs card prices from a Scryfall bulk file.

    Reads the file incrementally and updates prices
    only for cards that exist in the local database.
    """
    cards_by_scryfall_id = {
        card.scryfall_id: card
        for card in Card.objects.all()
    }

    updated = 0 

    with transaction.atomic():
        for bulk_card in iter_bulk_cards(bulk_file_path):
            scryfall_id = bulk_card.get("id")
            card = cards_by_scryfall_id.get(scryfall_id)

            if not card: 
                continue

            prices = bulk_card.get("prices", {})

            if card.finish == "foil":
                price = prices.get("usd_foil")
            else:
                price = prices.get("usd")

            if not price:
                continue

            price_decimal = Decimal(price)

            if card.price_usd != price_decimal:
                card.price_usd = price_decimal
                card.save(update_fields=["price_usd"])
                updated += 1

    return updated