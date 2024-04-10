from fastapi.routing import APIRouter

from random_generator.web.api import docs, monitoring, random

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(random.router)
