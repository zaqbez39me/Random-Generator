import pytest
from unittest.mock import patch, MagicMock
from random_generator.web.api.random.seed_fetchers import TimeSeedFetcher

@pytest.fixture
def mock_response():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "dateTime": "2024-04-22T12:00:00Z"
    }
    return mock_resp

@patch('requests.get')
def test_fetch_data(mock_get, mock_response):
    mock_get.return_value = mock_response
    data = TimeSeedFetcher._TimeSeedFetcher__fetch_data()
    assert data.dt.isoformat() == "2024-04-22T12:00:00+00:00"

def test_encode_data():
    time_data = TimeSeedFetcher.TimeAPIResponseModel(
        dateTime="2024-04-22T12:00:00Z"
    )
    seed = TimeSeedFetcher._TimeSeedFetcher__encode_data(time_data)
    assert seed == 33152

@patch('random_generator.web.api.random.seed_fetchers.TimeSeedFetcher._TimeSeedFetcher__fetch_data')
@patch('random_generator.web.api.random.seed_fetchers.TimeSeedFetcher._TimeSeedFetcher__encode_data')
def test_get_seed(mock_encode_data, mock_fetch_data):
    mock_fetch_data.return_value = MagicMock(
        dt="2024-04-22T12:00:00Z"
    )
    mock_encode_data.return_value = 61594
    seed = TimeSeedFetcher.get_seed()
    assert seed == 61594
