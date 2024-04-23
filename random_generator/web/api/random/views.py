from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from random_generator.web.api.random.seed_fetchers import RandomSource

router = APIRouter(prefix="/random")


class RandomSourcesResponse(BaseModel):
    """
    Response model for available random sources.

    This Pydantic BaseModel represents the response for retrieving the available
    random sources. It contains a single attribute `sources`, which is a list of
    strings representing the names of the available random sources.

    """

    sources: list[str]


class RandomNumberResponse(BaseModel):
    """
    Response model for random number generation.

    This Pydantic BaseModel represents the response for generating a random number.
    It contains a single attribute `random_number` representing the generated random
    number.

    """

    random_number: float


@router.get(
    "/sources",
    status_code=status.HTTP_200_OK,
    response_model=RandomSourcesResponse,
)
def get_random_sources() -> RandomSourcesResponse:
    """
    Get the available random sources.

    This function returns a RandomSourcesResponse object containing the names
    of all available random sources. It retrieves the names from the RandomSource
    enumeration.

    :returns:
        A RandomSourcesResponse object containing the names of available random sources.
    """
    return RandomSourcesResponse(sources=[source.name for source in RandomSource])


@router.get(
    "/{source}",
    status_code=status.HTTP_200_OK,
    response_model=RandomNumberResponse,
)
def generate_random_number(source: str) -> RandomNumberResponse:
    """
    Generate a random number based on the specified source.

    This function takes a source string as input and generates a random number
    based on the specified source. If the source is not found in the available
    sources, it raises an HTTPException with status code 400 (Bad Request).

    :param source:
        A string representing the source of the random number (e.g., "weather",
        "news", "time").

    :returns:
        A RandomNumberResponse object containing the generated random number.

    :raises HTTPException:
        If the specified source is not found.
    """
    if source not in RandomSource.__members__:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source not found",
        )

    return RandomNumberResponse(random_number=RandomSource[source].random())
