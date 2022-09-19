from sqlalchemy.orm import Session
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.cruds.user_crud import UserCRUD
from app.api.deps import get_db, init_redis
from app.clients.dadata_client import DadataClient
from app.schemas.user_schema import (
    UserSchemaOnGet,
    UserSchemaOnCreate,
    UserCreateSchema,
    UserBase,
    UserSchemaOnDelete,
)


users_api = APIRouter(tags=['users'], prefix='/users')


@users_api.post(
    path='/create',
    response_model=UserSchemaOnCreate,
    status_code=201
)
async def create_user_data(
        *,
        db: Session = Depends(get_db),
        user_data: UserCreateSchema,
) -> User:
    user = UserCRUD.get_user(
        db=db,
        obj_in=UserBase(phone_number=user_data.phone_number)
    )
    if user:
        updated_user = UserCRUD.update_user(
            db=db,
            obj_in=user_data,
            db_user=user
        )
        return updated_user
    created_user = UserCRUD.create_user(db=db, obj_in=user_data)
    return created_user


@users_api.post(
    path='/get',
    response_model=UserSchemaOnGet,
    status_code=200
)
async def get_user_data(
        *,
        db: Session = Depends(get_db),
        redis: Redis = Depends(init_redis),
        user_data: UserBase,
) -> UserSchemaOnGet:
    db_user = UserCRUD.get_user(db=db, obj_in=user_data)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User with phone number {phone_number} not found'.format(
                phone_number=user_data.phone_number,
            )
        )
    dadata_client = DadataClient(db_user=db_user, redis=redis)
    user = await dadata_client.get_user_data()
    return user


@users_api.post(
    path='/remove',
    response_model=UserSchemaOnDelete,
    status_code=201
)
async def delete_user_data(
        *,
        db: Session = Depends(get_db),
        user_data: UserBase,
) -> User:
    db_user = UserCRUD.get_user(db=db, obj_in=user_data)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User with phone number {phone_number} not found'.format(
                phone_number=user_data.phone_number,
            )
        )
    deleted_user = UserCRUD.remove_user(db=db, db_user=db_user)
    return deleted_user
