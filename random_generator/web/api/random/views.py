from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from random_generator.web.api.random.seed_fetchers import RandomSource

router = APIRouter(prefix="/random")


class RandomSourcesResponse(BaseModel):
    sources: list[str]


class RandomNumberResponse(BaseModel):
    random_number: float


@router.get(
    "/sources",
    status_code=status.HTTP_200_OK,
    response_model=RandomSourcesResponse,
)
def get_random_sources() -> RandomSourcesResponse:
    """
    Return the list of random sources.
    """

    return RandomSourcesResponse(sources=[source.name for source in RandomSource])


@router.get(
    "/{source}",
    status_code=status.HTTP_200_OK,
    response_model=RandomNumberResponse,
)
def generate_random_number(source: str):
    """
    Return the random number from given source.
    """

    if source not in RandomSource.__members__:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source not found",
        )

    return RandomNumberResponse(random_number=RandomSource[source].random())
