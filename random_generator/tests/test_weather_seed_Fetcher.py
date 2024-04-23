import pytest
from unittest.mock import patch, MagicMock
from random_generator.web.api.random.seed_fetchers import WeatherSeedFetcher


@pytest.fixture
def mock_response() -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "current": {
            "temperature_2m": 25.0
        }
    }
    return mock_resp


@patch('requests.get')
def test_fetch_data(mock_get: MagicMock, mock_response: MagicMock) -> None:
    mock_get.return_value = mock_response
    data = WeatherSeedFetcher._WeatherSeedFetcher__fetch_data()  # type: ignore[attr-defined]
    assert data.current.temperature == 25.0


def test_encode_data() -> None:
    weather_data = WeatherSeedFetcher.WeatherAPIResponseModel(
        current=WeatherSeedFetcher.WeatherAPIResponseModel.CurrentModel(
            temperature_2m=25.0
        )
    )
    seed = WeatherSeedFetcher._WeatherSeedFetcher__encode_data(weather_data)  # type: ignore[attr-defined]
    assert seed == 2015648683


@patch(
    'random_generator.web.api.random.seed_fetchers.WeatherSeedFetcher._WeatherSeedFetcher__fetch_data')
@patch(
    'random_generator.web.api.random.seed_fetchers.WeatherSeedFetcher._WeatherSeedFetcher__encode_data')
def test_get_seed(mock_encode_data: MagicMock, mock_fetch_data: MagicMock) -> None:
    mock_fetch_data.return_value = MagicMock(
        current=MagicMock(temperature=25.0)
    )
    mock_encode_data.return_value = 321394091
    seed = WeatherSeedFetcher.get_seed()
    assert seed == 321394091
