import ijson
from pathlib import Path

def iter_bulk_cards(bulk_file_path: Path):
    """
    Iterates over cards in a Scryfall bulk JSON file one by one.
    """
    with bulk_file_path.open("rb") as f:
        for card in ijson.items(f,"item"):
            yield card