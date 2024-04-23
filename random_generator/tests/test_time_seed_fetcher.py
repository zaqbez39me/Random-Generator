from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from random_generator.web.api.random.seed_fetchers import TimeSeedFetcher


@pytest.fixture
def mock_response() -> MagicMock:
    """
    Create a mocked response object for HTTP requests.

    This fixture creates a MagicMock object to mimic an HTTP response.
    It sets the status code to 200 and configures the json() method to
    return a sample JSON response containing a date and time.

    :returns:
        A MagicMock object representing the mocked HTTP response.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"dateTime": "2024-04-22T12:00:00Z"}
    return mock_resp


@patch("requests.get")
def test_fetch_data(mock_get: MagicMock, mock_response: MagicMock) -> None:
    """
    Test the fetching of time data.

    This function mocks the requests.get method to simulate a response,
    then calls the __fetch_data method of TimeSeedFetcher and asserts
    that the fetched time data's ISO-formatted datetime matches the expected
    value.

    :param mock_get:
        A MagicMock object representing the mocked requests.get function.
    :param mock_response:
        A MagicMock object representing the mocked response from requests.get.
    """
    mock_get.return_value = mock_response
    data = TimeSeedFetcher._TimeSeedFetcher__fetch_data()  # type: ignore[attr-defined]
    assert data.dt.isoformat() == "2024-04-22T12:00:00+00:00"


def test_encode_data() -> None:
    """
    Test the encoding of time data into a seed value.

    This function creates a sample time data object containing a specific datetime,
    and then calls the __encode_data method of TimeSeedFetcher to encode the time data
    into a seed value. The resulting seed is compared with the expected seed value.
    """
    time_data = TimeSeedFetcher.TimeAPIResponseModel(
        dateTime=datetime.fromisoformat("2024-04-22T12:00:00Z"),
    )
    seed = TimeSeedFetcher._TimeSeedFetcher__encode_data(time_data)  # type: ignore[attr-defined]
    assert seed == 33152


@patch(
    "random_generator.web.api.random.seed_fetchers.TimeSeedFetcher."
    "_TimeSeedFetcher__fetch_data",
)
@patch(
    "random_generator.web.api.random.seed_fetchers.TimeSeedFetcher."
    "_TimeSeedFetcher__encode_data",
)
def test_get_seed(mock_encode_data: MagicMock, mock_fetch_data: MagicMock) -> None:
    """
    Test the generation of a seed value for time data.

    This function mocks the fetch_data and encode_data methods to return a sample
    time data and a predetermined seed value, respectively. It then calls the
    get_seed method of TimeSeedFetcher and asserts that the generated seed matches
    the predetermined value.

    :param mock_encode_data:
        A MagicMock object representing the mocked encode_data function.
    :param mock_fetch_data:
        A MagicMock object representing the mocked fetch_data function.
    """
    mock_fetch_data.return_value = MagicMock(dt="2024-04-22T12:00:00Z")
    mock_encode_data.return_value = 61594
    seed = TimeSeedFetcher.get_seed()
    assert seed == 61594
