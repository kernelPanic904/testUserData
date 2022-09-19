from json import dumps

from aioredis import Redis
from httpx import AsyncClient
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.schemas.user_schema import UserSchemaOnGet
from app.core.config import settings


class DadataClient:
    def __init__(self, db_user: User, redis: Redis) -> None:
        self.db_user = db_user
        self.redis = redis

    async def get_country_info(self) -> dict:
        async with AsyncClient() as client:
            dadata_query = {"query": self.db_user.country}
            headers = {
                'Authorization': "Token {token}".format(
                    token=settings.DADATA_API_KEY
                ),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            response = await client.post(
                url=settings.DADATA_COUNTRY_URL,
                content=dumps(dadata_query),
                headers=headers,
            )
            return response.json()

    async def get_country_code(self) -> str:
        country_info = await self.get_country_info()
        try:
            country_code = country_info['suggestions'][0]['data']['code']
        except Exception:
            raise HTTPException(status_code=404, detail='Not found')
        return country_code

    async def get_updated_user_data(
            self,
            country_code: str
    ) -> UserSchemaOnGet:
        user_data: dict = jsonable_encoder(self.db_user)
        user = UserSchemaOnGet(**user_data)
        user.country_code = country_code
        return user

    async def get_user_data(self) -> UserSchemaOnGet:
        cached_country_code = await self.redis.get(self.db_user.country)
        if not cached_country_code:
            country_code = await self.get_country_code()
            await self.redis.set(self.db_user.country, country_code)
            return await self.get_updated_user_data(country_code=country_code)
        return await self.get_updated_user_data(
            country_code=cached_country_code
        )
