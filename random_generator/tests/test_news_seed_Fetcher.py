from typing import Callable

import pytest
from unittest.mock import patch, MagicMock

from random_generator.web.api.random.seed_fetchers import NewsSeedFetcher


@pytest.fixture
def mock_response() -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"articles": [{"title": "Sample Article Title"}]}
    return mock_resp


@patch("requests.get")
def test_fetch_data(mock_get: MagicMock, mock_response: MagicMock) -> None:
    mock_get.return_value = mock_response
    data = NewsSeedFetcher._NewsSeedFetcher__fetch_data()  # type: ignore[attr-defined]
    assert data.articles[0].title == "Sample Article Title"


@patch("random.random")
def test_encode_data(mock_random: MagicMock) -> None:
    # Set the return value of random.random() to a fixed value for consistent testing
    mock_random.return_value = 0.123456789

    news_data = NewsSeedFetcher.NewsAPIResponseModel(
        articles=[
            NewsSeedFetcher.NewsAPIResponseModel.ArticleModel(
                title="Sample Article Title"
            )
        ]
    )
    seed = NewsSeedFetcher._NewsSeedFetcher__encode_data(  # type: ignore[attr-defined]
        news_data
    )

    # Calculate the expected seed value based on the mocked random.random() value
    expected_seed = int(
        hash("Sample Article Title") if news_data.articles else int(0.123456789)
    ) % (2**16)

    assert seed == expected_seed


@patch(
    "random_generator.web.api.random.seed_fetchers.NewsSeedFetcher._NewsSeedFetcher__fetch_data"
)
@patch(
    "random_generator.web.api.random.seed_fetchers.NewsSeedFetcher._NewsSeedFetcher__encode_data"
)
def test_get_seed(mock_encode_data: MagicMock, mock_fetch_data: MagicMock) -> None:
    mock_fetch_data.return_value = MagicMock(
        articles=[MagicMock(title="Sample Article Title")]
    )
    mock_encode_data.return_value = 40608
    seed = NewsSeedFetcher.get_seed()
    assert seed == 40608
