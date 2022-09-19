from fastapi import APIRouter

from app.core.config import settings
from app.api.api_v1.users_api import users_api

api_v1_router = APIRouter(prefix=settings.API_V1_STR)
api_v1_router.include_router(users_api)
