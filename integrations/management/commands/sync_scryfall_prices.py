from django.core.management.base import BaseCommand

from pathlib import Path
import tempfile

from integrations.services.scryfall_client import get_default_cards_bulk_url
from integrations.services.bulk_downloader import download_bulk_file
from integrations.services.price_sync_service import sync_card_prices_from_bulk


class Command(BaseCommand):
    help = "Sync prices from scryfall"

    def handle(self, *args, **options):
        self.stdout.write("Starting Scryfall price sync...")
        
        self.stdout.write("Fetching bulk metadata...")
        bulk_url = get_default_cards_bulk_url()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            bulk_path = Path(tmp.name)

        self.stdout.write("Downloading bulk file...")
        download_bulk_file(bulk_url, bulk_path)

        self.stdout.write("Syncing prices...")
        updated = sync_card_prices_from_bulk(bulk_path)

        bulk_path.unlink(missing_ok=True)

        self.stdout.write(
            self.style.SUCCESS(f"Sync complete. Updated {updated} cards.")
        )
