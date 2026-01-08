from pathlib import Path 
import requests

def download_bulk_file(download_url: str, destination: Path):
    """
    Downloads a large file from a URL and saves it to disk in chunks.
    """
    response = requests.get(
        download_url,
        stream=True,
        timeout=60
    )
    response.raise_for_status()

    with destination.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)