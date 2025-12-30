from cards.models import Card
from integrations.scryfall import fetch_card

def import_exact_mtg_card(
        *,
        set_code: str,
        collector_number: str,
) -> Card:
    """
    Import an exact Magic: The Gathering card printing into the database.

    This function retrieves a single, exact card printing from the Scryfall API
    using the provided set code and collector number, validates that the
    requested finish (foil / nonfoil) is available, and ensures the card
    exists in the local database.

    If the card already exists, it is returned without modification.
    If it does not exist, it is created and saved automatically.

    This function is **idempotent**:
    calling it multiple times with the same parameters will never create
    duplicate database records.

    Parameters
    ----------
    set_code : str
        The Scryfall set code identifying the card set (e.g. "sld", "cmm").
        This should match Scryfall's canonical set codes.

    collector_number : str
        The exact collector number as defined by Scryfall.
        This value must match exactly and may contain letters (e.g. "2008").

    Returns
    -------
    Card
        A Django `Card` model instance representing the imported card.

    Raises
    ------
    ValueError
        - If no card is found for the given set code and collector number.
        - If the requested finish is not available for the card.

    Notes
    -----
    - This function performs a database write when a new card is created.
    - Card uniqueness is enforced using the Scryfall card ID.
    - Price fields may be null if market data is unavailable.

    Example
    -------
    >>> card = import_exact_mtg_card(
    ...     set_code="sld",
    ...     collector_number="2008",
    ...     finish="foil"
    ... )
    >>> card.name
    'Uncivil Unrest'
    """
    data = fetch_card(set_code,collector_number)

    if not data:
        raise ValueError("Card not found")
    
    available_finishes = data.get("finishes", [])

    if "foil" in available_finishes:
        chosen_finish = "foil"
    elif "nonfoil" in available_finishes:
        chosen_finish = "nonfoil"
    else:
        chosen_finish = available_finishes[0] if available_finishes else None
    
    card, _ = Card.objects.get_or_create(
        scryfall_id=data["id"],
        defaults={
            "name": data["name"],
            "set_code": data["set"],
            "set_name": data["set_name"],
            "collector_number": data["collector_number"],
            "finish": chosen_finish,
            "rarity": data["rarity"],
            "image_url": data["image_uris"]["normal"],
            "price_usd": (
                data["prices"]["usd_foil"]
                if chosen_finish == "foil"
                else data["prices"]["usd"]
            ),
        }
    )

    return card