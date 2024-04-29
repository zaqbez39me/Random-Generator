import datetime
from unittest.mock import MagicMock, patch

from freezegun import freeze_time
from pytest import fixture

from random_generator.web.api.random.seed_fetchers import NewsSeedFetcher


@fixture
def mock_response() -> MagicMock:
    """
    Fixture function for mocking HTTP responses.

    Determine which files are about to be committed and run Flake8 over them
    to check for violations.

    :returns:
        MagicMock: A MagicMock object simulating an HTTP response with status code 200
        and JSON data containing a sample article title.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"articles": [{"title": "Sample Article Title"}]}
    return mock_resp


@patch("requests.get")
def test_fetch_data(mock_get: MagicMock, mock_response: MagicMock) -> None:
    """
    Test the data fetching functionality of NewsSeedFetcher.

    This function mocks the requests. get method to simulate a response,
    then calls the __fetch_data method of NewsSeedFetcher and asserts
    that the fetched data's first article title matches the expected
    value.

    :param mock_get:
        A MagicMock object representing the mocked requests. get function.
    :param mock_response:
        A MagicMock object representing the mocked response from requests.get.
    """
    mock_get.return_value = mock_response
    data = NewsSeedFetcher._NewsSeedFetcher__fetch_data()  # type: ignore[attr-defined]
    assert data.articles[0].title == "Sample Article Title"


@patch(
    "random_generator.web.api.random.seed_fetchers.NewsSeedFetcher._NewsSeedFetcher"
    "__fetch_data",
)
@freeze_time("2024-04-29 11:46:10")
def test_encode_data(mock_fetch_data: MagicMock) -> None:
    """
    Test the encoding of news data into a seed value.

    This function mocks the random. random method to ensure consistent testing.
    It gets a seed value using the get_seed method of NewsSeedFetcher. The
    resulting seed is compared with the expected seed value calculated based
    on the mocked api return value.

    :param mock_fetch_data:
        A MagicMock object representing the mocked fetcher fetch data method.
    """
    # Set the return value of mock_fetcher.__fetch_data to a
    # fixed value for consistent testing
    mock_fetch_data.return_value = NewsSeedFetcher.NewsAPIResponseModel(
        articles=[
            NewsSeedFetcher.NewsAPIResponseModel.ArticleModel(
                title="Sample Article Title",
            ),
        ],
    )
    seed = NewsSeedFetcher.get_seed()
    mod_num = 1_000_000_007
    epoch = datetime.datetime.utcfromtimestamp(0)
    encoded_seed = hash("Sample Article Title")
    expected_seed = (
        encoded_seed * int((datetime.datetime.now() - epoch).total_seconds() * 1_000)
    ) % mod_num
    assert seed == expected_seed


@patch(
    "random_generator.web.api.random.seed_fetchers.NewsSeedFetcher._NewsSeedFetcher"
    "__fetch_data",
)
@patch(
    "random_generator.web.api.random.seed_fetchers.NewsSeedFetcher._NewsSeedFetcher"
    "__encode_data",
)
def test_get_seed(mock_encode_data: MagicMock, mock_fetch_data: MagicMock) -> None:
    """
    Test the generation of a seed value for news data.

    This function mocks the fetch_data and encode_data methods to return a sample
    news data and a predetermined seed value, respectively. It then calls the
    get_seed method of NewsSeedFetcher and asserts that the generated seed matches
    the predetermined value.

    :param mock_encode_data:
        A MagicMock object representing the mocked encode_data function.
    :param mock_fetch_data:
        A MagicMock object representing the mocked fetch_data function.
    """
    mock_fetch_data.return_value = MagicMock(
        articles=[MagicMock(title="Sample Article Title")],
    )
    mock_encode_data.return_value = 40608
    seed = NewsSeedFetcher.get_seed()
    assert seed == 40608
