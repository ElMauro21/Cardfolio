from cards.models import Card
from integrations.scryfall import fetch_card

def import_exact_mtg_card(
        *,
        set_code: str,
        collector_number: str,
        is_foil: bool,
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

    if is_foil:
        if "foil" not in available_finishes:
            raise ValueError("This card does not have a foil version")
        chosen_finish="foil"
    else:
        if "nonfoil" not in available_finishes:
            raise ValueError("This card does not have a non-foil version")
        chosen_finish = "nonfoil"

    price = (
        data["prices"]["usd_foil"]
        if chosen_finish == "foil"
        else data["prices"]["usd"]
    )

    card, _ = Card.objects.get_or_create(
        scryfall_id=data["id"],
        finish=chosen_finish,
        defaults={
            "name": data["name"],
            "set_code": data["set"],
            "set_name": data["set_name"],
            "collector_number": data["collector_number"],
            "rarity": data["rarity"],
            "image_url": data["image_uris"]["normal"],
            "price_usd": price,
        }
    )

    return card