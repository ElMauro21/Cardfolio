import requests

SCRYFALL_BASE_URL = "https://api.scryfall.com"
SCRYFALL_TIMEOUT = 10

def fetch_card(set_code: str, collector_number: str):
    """
    Fetch a single Magic: The Gathering card from the Scryfall API
    using an exact set code and collector number.

    This function calls the Scryfall endpoint:
        GET /cards/{set_code}/{collector_number}

    It is designed to retrieve a **single, exact printing** of a card.
    No database operations are performed here — this function only
    communicates with the external API.

    Parameters
    ----------
    set_code : str
        The Scryfall set code (e.g. "sld", "cmm", "khm").
        This should be lowercase and match Scryfall's canonical set codes.

    collector_number : str
        The exact collector number as defined by Scryfall.
        This may contain letters (e.g. "2008a") and must match exactly.

    Returns
    -------
    dict | None
        - A dictionary containing the card data returned by Scryfall
          if the request is successful (HTTP 200).
        - None if the card is not found or the request fails.

    Notes
    -----
    - This function does NOT raise exceptions for HTTP errors.
      It returns None instead, allowing higher-level services
      to decide how to handle missing or invalid cards.
    - Network timeouts are limited to 10 seconds.
    - Finish (foil / nonfoil) validation is NOT handled here.

    Example
    -------
    >>> data = fetch_card("sld", "2008")
    >>> data["name"]
    'Uncivil Unrest'
    """
    url = f"{SCRYFALL_BASE_URL}/cards/{set_code}/{collector_number}"

    response = requests.get(url, timeout=SCRYFALL_TIMEOUT)

    if response.status_code != 200:
        return None
    
    return response.json()