from typing import Generator

import pytest
from fastapi.testclient import TestClient

from random_generator.web.application import get_app


@pytest.fixture
def server() -> Generator[TestClient, None, None]:
    """
    Fixture for creating a TestClient instance for testing.

    This fixture sets up the test environment by creating a TestClient
    instance with the application returned by the get_app function.
    The TestClient instance can be used in test functions to simulate
    requests to the server.

    :yields:
        A generator that yields a TestClient instance.
    """
    app = get_app()
    yield TestClient(app)


def test_get_sources_endpoint(server: TestClient) -> None:
    """
    Test the '/api/random/sources' endpoint.

    This function sends a GET request to the '/api/random/sources' endpoint
    using the provided TestClient instance. It then verifies that the response
    status code is 200 and that the returned JSON data contains the expected
    sources.

    :param server:
        A TestClient instance representing the test server.
    """
    url: str = "/api/random/sources"
    expected_data: dict[str, list[str]] = {"sources": ["weather", "time", "news"]}
    response = server.get(url)
    assert response.status_code == 200
    assert response.json() == expected_data


def test_weather_endpoint_returns_random_number(server: TestClient) -> None:
    """
    Test the '/api/random/weather' endpoint.

    This function sends a GET request to the '/api/random/weather' endpoint
    using the provided TestClient instance. It then verifies that the response
    status code is 200 and that the returned JSON data contains a 'random_number'
    field with a value between 0 and 1.

    :param server:
        A TestClient instance representing the test server.
    """
    url: str = "/api/random/weather"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1


def test_news_endpoint_returns_random_number(server: TestClient) -> None:
    """
    Test the '/api/random/news' endpoint.

    This function sends a GET request to the '/api/random/news' endpoint
    using the provided TestClient instance. It then verifies that the response
    status code is 200 and that the returned JSON data contains a 'random_number'
    field with a value between 0 and 1.

    :param server:
        A TestClient instance representing the test server.
    """
    url: str = "/api/random/news"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1


def test_time_endpoint_returns_random_number(server: TestClient) -> None:
    """
    Test the '/api/random/time' endpoint.

    This function sends a GET request to the '/api/random/time' endpoint
    using the provided TestClient instance. It then verifies that the response
    status code is 200 and that the returned JSON data contains a 'random_number'
    field with a value between 0 and 1.

    :param server:
        A TestClient instance representing the test server.
    """
    url: str = "/api/random/time"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1
