from typing import AsyncIterator

from sqlalchemy.orm import Session
from aioredis import Redis, from_url

from app.db.session import SessionLocal
from app.core.config import settings


async def get_db() -> AsyncIterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_redis() -> AsyncIterator[Redis]:
    redis: Redis = await from_url(settings.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()
