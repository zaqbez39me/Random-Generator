from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time

from random_generator.web.api.random.seed_fetchers import WeatherSeedFetcher


@pytest.fixture
def mock_response() -> MagicMock:
    """
    Create a mocked response object for HTTP requests.

    This fixture creates a MagicMock object to mimic an HTTP response.
    It sets the status code to 200 and configures the json() method to
    return a sample JSON response containing temperature data.

    :returns:
        A MagicMock object representing the mocked HTTP response.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"current": {"temperature_2m": 25.0}}
    return mock_resp


@patch("requests.get")
def test_fetch_data(mock_get: MagicMock, mock_response: MagicMock) -> None:
    """
    Test the fetching of weather data.

    This function mocks the requests.get method to simulate a response,
    then calls the __fetch_data method of WeatherSeedFetcher and asserts
    that the fetched weather data's current temperature matches the expected
    value.

    :param mock_get:
        A MagicMock object representing the mocked requests. get function.
    :param mock_response:
        A MagicMock object representing the mocked response from requests.get.
    """
    mock_get.return_value = mock_response
    data = WeatherSeedFetcher._WeatherSeedFetcher__fetch_data()  # type: ignore[attr-defined]
    assert data.current.temperature == 25


@freeze_time("2024-04-29 11:46:10")
def test_encode_data() -> None:
    """
    Test the encoding of weather data into a seed value.

    This function creates a sample weather data object containing the current
    temperature and then calls the __encode_data method of WeatherSeedFetcher
    to encode the weather data into a seed value. The resulting seed is compared
    with the expected seed value.
    """
    weather_data = WeatherSeedFetcher.WeatherAPIResponseModel(
        current=WeatherSeedFetcher.WeatherAPIResponseModel.CurrentModel(
            temperature_2m=25.0,
        ),
    )
    seed = WeatherSeedFetcher._WeatherSeedFetcher__encode_data(
        weather_data
    )  # type: ignore[attr-defined]
    assert seed == 859778956


@patch(
    "random_generator.web.api.random.seed_fetchers.WeatherSeedFetcher."
    "_WeatherSeedFetcher__fetch_data",
)
@patch(
    "random_generator.web.api.random.seed_fetchers.WeatherSeedFetcher."
    "_WeatherSeedFetcher__encode_data",
)
def test_get_seed(mock_encode_data: MagicMock, mock_fetch_data: MagicMock) -> None:
    """
    Test the generation of a seed value for weather data.

    This function mocks the fetch_data and encode_data methods to return a sample
    weather data and a predetermined seed value, respectively. It then calls the
    get_seed method of WeatherSeedFetcher and asserts that the generated seed matches
    the predetermined value.

    :param mock_encode_data:
        A MagicMock object representing the mocked encode_data function.
    :param mock_fetch_data:
        A MagicMock object representing the mocked fetch_data function.
    """
    mock_fetch_data.return_value = MagicMock(current=MagicMock(temperature=25.0))
    mock_encode_data.return_value = 321394091
    seed = WeatherSeedFetcher.get_seed()
    assert seed == 321394091
