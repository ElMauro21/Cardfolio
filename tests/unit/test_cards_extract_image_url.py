import pytest
from cards.services.card_importer import extract_image_url

@pytest.mark.unit
def test_extract_image_url_from_image_uris():
    data={
        "image_uris": {
            "normal": "https://example.com/card.jpg"
        }
    }

    result = extract_image_url(data)

    assert result == "https://example.com/card.jpg"

@pytest.mark.unit 
def test_extract_image_url_from_card_faces():
    data = {
        "card_faces": [
            {
                "image_uris": {
                    "normal": "https://example.com/face.jpg"
                }
            }
        ]
    }
    result = extract_image_url(data)

    assert result == "https://example.com/face.jpg"
     
@pytest.mark.unit
def test_extract_image_url_returns_none_when_no_images():
    data = {}

    result = extract_image_url(data)

    assert result is None