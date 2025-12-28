from cards.models import Card
from integrations.scryfall import fetch_card

def import_exact_mtg_card(
        *,
        set_code: str,
        collector_number: str,
        finish: str
) -> Card:
    
    data = fetch_card(set_code,collector_number)

    if not data:
        raise ValueError("Card not found")
    
    if finish not in data.get("finishes",[]):
        raise ValueError("Requested finish not available for this card")
    
    card, _ = Card.objects.get_or_create(
        scryfall_id=data["id"],
        defaults={
            "name": data["name"],
            "set_code": data["set"],
            "set_name": data["set_name"],
            "collector_number": data["collector_number"],
            "finish": finish,
            "rarity": data["rarity"],
            "image_url": data["image_uris"]["normal"],
            "price_usd": (
                data["prices"]["usd_foil"]
                if finish == "foil"
                else data["prices"]["usd"]
            ),
        }
    )

    return card