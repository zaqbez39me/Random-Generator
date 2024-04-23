import abc
import random
from datetime import datetime
from enum import Enum

import requests
from pydantic import BaseModel, Field
from requests import Response

from random_generator.settings import settings


class SeedFetcher(abc.ABC):
    def get_seed(self) -> int:
        pass


class WeatherSeedFetcher(SeedFetcher):
    class WeatherAPIResponseModel(BaseModel):
        class CurrentModel(BaseModel):
            temperature: float = Field(alias="temperature_2m")

        current: CurrentModel

    @classmethod
    def __fetch_data(cls) -> WeatherAPIResponseModel:
        response: Response = requests.get(
            url="https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": settings.weather_latitude,
                "longitude": settings.weather_longitude,
                "current": "temperature_2m",
            },
            timeout=settings.requests_timeout,
        )
        if response.status_code != 200:
            raise ValueError("Weather api did not response successfully")
        data = response.json()
        return cls.WeatherAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: WeatherAPIResponseModel) -> int:
        return round(424223331 * float(data.current.temperature)) % (2**32)

    @classmethod
    def get_seed(cls) -> int:
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class TimeSeedFetcher(SeedFetcher):
    class TimeAPIResponseModel(BaseModel):
        dt: datetime = Field(alias="dateTime")

    @classmethod
    def __fetch_data(cls) -> TimeAPIResponseModel:
        response: Response = requests.get(
            url="https://www.timeapi.io/api/Time/current/zone",
            params={
                "timeZone": settings.time_zone,
            },
            timeout=settings.requests_timeout,
        )
        if response.status_code != 200:
            raise ValueError("Time api did not response successfully")
        data = response.json()
        return cls.TimeAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: TimeAPIResponseModel) -> int:
        return round(data.dt.timestamp() * 13134) % (2**16)

    @classmethod
    def get_seed(cls) -> int:
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class NewsSeedFetcher(SeedFetcher):
    class NewsAPIResponseModel(BaseModel):
        class ArticleModel(BaseModel):
            title: str

        articles: list[ArticleModel]

    @classmethod
    def __fetch_data(cls) -> NewsAPIResponseModel:
        response: Response = requests.get(
            url="https://newsapi.org/v2/everything",
            params={
                "apiKey": settings.news_api_key,
                "q": settings.news_query,
                "sortBy": "publishedAt",
                "page": 1,
                "pageSize": 1,
            },
            timeout=settings.requests_timeout,
        )
        if response.status_code != 200:
            raise ValueError("News api did not response successfully")
        data = response.json()
        return cls.NewsAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: NewsAPIResponseModel) -> int:
        return int(
            hash(data.articles[0].title) if data.articles else int(random.random()),
        ) % (2**16)
    ##

    @classmethod
    def get_seed(cls) -> int:
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class RandomSource(Enum):
    weather = WeatherSeedFetcher
    time = TimeSeedFetcher
    news = NewsSeedFetcher

    def __init__(self, fetcher: SeedFetcher):
        self.fetcher = fetcher

    def random(self):
        rand = random.Random(x=random.random() + self.fetcher.get_seed())
        return rand.random()
