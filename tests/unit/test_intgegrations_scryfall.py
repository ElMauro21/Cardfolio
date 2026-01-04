import pytest

from integrations.scryfall import fetch_card, SCRYFALL_BASE_URL, SCRYFALL_TIMEOUT

@pytest.mark.unit
def test_fetch_card_returns_data_when_status_200(mocker):
    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "name": "Black Lotus",
        "set": "lea",
        "collector_number": "233"
    }

    mocker.patch(
        "integrations.scryfall.requests.get",
        return_value = fake_response
    )

    result = fetch_card("lea","233")

    assert result["name"] == "Black Lotus"
    assert result["set"] == "lea"
    assert result["collector_number"] == "233"

@pytest.mark.unit
def test_fetch_card_returns_none_when_status_404(mocker):
    fake_response = mocker.Mock()
    fake_response.status_code = 404

    mocker.patch(
        "integrations.scryfall.requests.get",
        return_value = fake_response
    )

    result = fetch_card("lea","999")

    assert result is None

@pytest.mark.unit
def test_fetch_Card_calls_scryfall_with_correct_url_and_timeout(mocker):
    fake_response = mocker.Mock()
    fake_response.status_code = 200 
    fake_response.json.return_value = {}

    mocked_get = mocker.patch(
        "integrations.scryfall.requests.get",
        return_value=fake_response
    )

    fetch_card("lea","233")

    mocked_get.assert_called_once_with(
        f"{SCRYFALL_BASE_URL}/cards/lea/233",
        timeout = SCRYFALL_TIMEOUT
    )