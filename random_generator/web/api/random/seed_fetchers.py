import abc
import random
from datetime import datetime
from enum import Enum

import requests  # type: ignore[import-untyped]
from pydantic import BaseModel, Field
from requests import Response

from random_generator.settings import settings


class SeedFetcher(abc.ABC):
    """
    Abstract base class for seed fetchers.

    This abstract base class defines the interface for classes responsible for fetching
    seed values used in generating random data. Subclasses must implement the `get_seed`
    method to provide specific implementations for fetching seed values.

    """

    @abc.abstractmethod
    def get_seed(self) -> int:
        """
        Abstract method to get a seed value.

        This method should be implemented by subclasses to provide functionality
        for fetching a seed value used in generating random data.
        """


class WeatherSeedFetcher(SeedFetcher):
    """
    Fetches weather data from the Open-Meteo API and provides methods to generate seed values.

    This class inherits from SeedFetcher and provides functionality to fetch weather data
    from the Open-Meteo API and generate seed values based on the fetched data. It includes
    methods to fetch weather data (__fetch_data), encode the data into seed values
    (__encode_data), and retrieve a seed value for generating random data (get_seed).

    """

    class WeatherAPIResponseModel(BaseModel):
        class CurrentModel(BaseModel):
            temperature: float = Field(alias="temperature_2m")

        current: CurrentModel

    @classmethod
    def __fetch_data(cls) -> WeatherAPIResponseModel:
        """
        Fetch weather data from the Open-Meteo API.

        This class method sends a GET request to the Open-Meteo API to fetch
        weather data. It extracts the response JSON and parses it into
        a WeatherAPIResponseModel object.

        :returns:
            A WeatherAPIResponseModel object containing weather data.

        :raises ValueError:
            If the Open-Meteo API does not respond successfully (status code other than 200).
        """
        response: Response = requests.get(
            url="https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": settings.weather_latitude,
                "longitude": settings.weather_longitude,
                "current": "temperature_2m",
            },
            timeout=settings.requests_timeout,
        )
        ok = 200
        if response.status_code != ok:
            raise ValueError("Weather api did not respond successfully")
        data = response.json()
        return cls.WeatherAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: WeatherAPIResponseModel) -> int:
        """
        Encode weather data into a seed value.

        This class method takes a WeatherAPIResponseModel object as input and encodes
        its data into a seed value. It multiplies the temperature from the response data
        by a constant factor and takes the modulo of the result with 2 raised to the power
        of 32 to obtain the seed value.

        :param data:
            A WeatherAPIResponseModel object containing weather data.
        :returns:
            An integer representing the encoded seed value.
        """
        mod_num = 1_000_000_007
        epoch = datetime.utcfromtimestamp(0)
        return (
            round(
                float(data.current.temperature)
                * (datetime.now() - epoch).total_seconds(),
            )
            % mod_num
        )

    @classmethod
    def get_seed(cls) -> int:
        """
        Get a seed value for generating random data.

        This class method fetches data specific to the class using the
        __fetch_data method and encodes it into a seed value using the
        __encode_data method. The resulting seed value is returned.

        :returns:
            An integer representing the seed value.
        """
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class TimeSeedFetcher(SeedFetcher):
    """
    Fetches time data from the Time API and provides methods to generate seed values.

    This class inherits from SeedFetcher and provides functionality to fetch time data
    from the Time API and generate seed values based on the fetched data. It includes
    methods to fetch time data (__fetch_data), encode the data into seed values
    (__encode_data), and retrieve a seed value for generating random data (get_seed).

    """

    class TimeAPIResponseModel(BaseModel):
        dt: datetime = Field(alias="dateTime")

    @classmethod
    def __fetch_data(cls) -> TimeAPIResponseModel:
        """
        Fetch time data from the Time API.

        This class method sends a GET request to the Time API to fetch
        time data. It extracts the response JSON and parses it into
        a TimeAPIResponseModel object.

        :returns:
            A TimeAPIResponseModel object containing time data.

        :raises ValueError:
            If the Time API does not respond successfully (status code other than 200).
        """
        response: Response = requests.get(
            url="https://www.timeapi.io/api/Time/current/zone",
            params={
                "timeZone": settings.time_zone,
            },
            timeout=settings.requests_timeout,
        )
        ok = 200
        if response.status_code != ok:
            raise ValueError("Time api did not respond successfully")
        data = response.json()
        return cls.TimeAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: TimeAPIResponseModel) -> int:
        """
        Encode time data into a seed value.

        This class method takes a TimeAPIResponseModel object as input and encodes
        its data into a seed value. It uses the timestamp of the datetime object
        from the response data and applies a multiplication factor. The resulting
        seed value is obtained by taking the modulo of the multiplied timestamp
        with 2 raised to the power of 16.

        :param data:
            A TimeAPIResponseModel object containing time data.
        :returns:
            An integer representing the encoded seed value.
        """
        mod_num = 1_000_000_007
        mult = 1_000_000_009
        return round(data.dt.timestamp() * mult) % mod_num

    @classmethod
    def get_seed(cls) -> int:
        """
        Get a seed value for generating random data.

        This class method fetches data specific to the class using the
        __fetch_data method and encodes it into a seed value using the
        __encode_data method. The resulting seed value is returned.

        :returns:
            An integer representing the seed value.
        """
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class NewsSeedFetcher(SeedFetcher):
    """
    Fetches news data from the News API and provides methods to generate seed values.

    This class inherits from SeedFetcher and provides functionality to fetch news data
    from the News API and generate seed values based on the fetched data. It includes
    methods to fetch news data (__fetch_data), encode the data into seed values
    (__encode_data), and retrieve a seed value for generating random data (get_seed).
    """

    class NewsAPIResponseModel(BaseModel):
        class ArticleModel(BaseModel):
            title: str

        articles: list[ArticleModel]

    @classmethod
    def __fetch_data(cls) -> NewsAPIResponseModel:
        """
        Fetch news data from the News API.

        This class method sends a GET request to the News API to fetch
        news data. It extracts the response JSON and parses it into
        a NewsAPIResponseModel object.

        :returns:
            A NewsAPIResponseModel object containing news data.

        :raises ValueError:
            If the News API does not respond successfully (status code other than 200).
        """
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
        ok = 200
        if response.status_code != ok:
            raise ValueError("News api did not respond successfully")
        data = response.json()
        return cls.NewsAPIResponseModel.parse_obj(data)

    @classmethod
    def __encode_data(cls, data: NewsAPIResponseModel) -> int:
        """
        Encode news data into a seed value.

        This class method takes a NewsAPIResponseModel object as input and encodes
        its data into a seed value. If the data contains articles, it hashes the
        title of the first article; otherwise, it uses a random float value. The
        resulting seed value is an integer obtained by taking the modulo of the hash
        or random value with 2 raised to the power of 16.

        :param data:
            A NewsAPIResponseModel object containing news data.
        :returns:
            An integer representing the encoded seed value.
        """
        mod_num = 1_000_000_007
        if data.articles:
            encoded_seed = hash(data.articles[0].title)
        else:
            encoded_seed = random.randint(1, mod_num)
        epoch = datetime.utcfromtimestamp(0)
        return (
            encoded_seed * int((datetime.now() - epoch).total_seconds() * 1_000)
        ) % mod_num

    @classmethod
    def get_seed(cls) -> int:
        """
        Get a seed value for generating random data.

        This class method fetches data specific to the class using the
        __fetch_data method and encodes it into a seed value using the
        __encode_data method. The resulting seed value is returned.

        :returns:
            An integer representing the seed value.
        """
        data = cls.__fetch_data()
        return cls.__encode_data(data)


class RandomSource(Enum):
    """
    Enumeration of random data sources.

    This enum defines different sources of random data, each associated
    with a specific SeedFetcher subclass. It provides a method to generate
    random float values using the associated fetcher's seed.

    Attributes:
        weather: A source of weather-related random data.
        time: A source of time-related random data.
        news: A source of news-related random data.
    """

    weather = WeatherSeedFetcher
    time = TimeSeedFetcher
    news = NewsSeedFetcher

    def __init__(self, fetcher: SeedFetcher):
        self.fetcher = fetcher

    def random(self) -> float:
        """
        Generate a random float.

        This method generates a random float value using the built-in
        random module. The random number generator is seeded with a
        value derived from the sum of a random float and the seed
        obtained from the fetcher's get_seed method.

        :returns:
            A random float value between 0 and 1.
        """
        rand = random.Random(x=self.fetcher.get_seed())
        return rand.random()
