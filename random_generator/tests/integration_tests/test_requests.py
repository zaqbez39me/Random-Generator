import pytest
from fastapi.testclient import TestClient
from random_generator.web.application import get_app
from typing import Generator

@pytest.fixture
def server() -> Generator[TestClient, None, None]:
    app = get_app()
    yield TestClient(app)

def test_get_sources_endpoint_returns_expected_data(server: TestClient) -> None:
    url: str = "/api/random/sources"
    expected_data: dict[str, list[str]] = {"sources": ["weather", "time", "news"]}
    response = server.get(url)
    assert response.status_code == 200
    assert response.json() == expected_data

def test_weather_endpoint_returns_random_number_in_segment(server: TestClient) -> None:
    url: str = "/api/random/weather"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1

def test_news_endpoint_returns_random_number_in_segment(server: TestClient) -> None:
    url: str = "/api/random/news"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1

def test_time_endpoint_returns_random_number_in_segment(server: TestClient) -> None:
    url: str = "/api/random/time"
    response = server.get(url)
    assert response.status_code == 200
    data: dict[str, float] = response.json()
    assert "random_number" in data
    assert 0 < data["random_number"] < 1
