import requests

SCRYFALL_APY_URL = "https://api.scryfall.com"

def get_bulk_metadata():
    """
    Fetches metadata about Scryfall bulk data files.
    """
    response = requests.get(
        f"{SCRYFALL_APY_URL}/bulk-data",
        timeout=15,
    )

    response.raise_for_status()

    return response.json()

def get_default_cards_bulk_url():
    """
    Return the download URL for Scryfall's default cards bulk data.
    """
    metadata = get_bulk_metadata()
    
    for item in metadata["data"]:
        if item["type"] == "default_cards":
            return item["download_uri"]
        
    raise RuntimeError("Default cards bulk data not found")