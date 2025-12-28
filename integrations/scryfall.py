import requests

SCRYFALL_BASE_URL = "https://api.scryfall.com"

def fetch_card(set_code: str, collector_number: str):
    url = f"{SCRYFALL_BASE_URL}/cards/{set_code}/{collector_number}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None
    
    return response.json()